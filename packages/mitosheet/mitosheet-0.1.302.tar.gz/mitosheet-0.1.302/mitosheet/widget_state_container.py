#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.

import json
import uuid 
from copy import copy, deepcopy
import pandas as pd
from typing import List

from mitosheet.errors import make_execution_error
from mitosheet.steps.column_steps.set_column_formula import SET_COLUMN_FORMULA_EVENT, SET_COLUMN_FORMULA_STEP_TYPE
from mitosheet.steps.filter import execute_filter_column
from mitosheet.steps import EVENT_TYPE_TO_STEP, STEP_TYPE_TO_STEP
from mitosheet.updates import UPDATES
from mitosheet.steps.initalize import execute_initialize_step
from mitosheet.preprocessing import PREPROCESS_STEPS
from mitosheet.utils import dfs_to_json, get_new_id
from mitosheet.transpiler.transpile import transpile
from mitosheet.user import get_user_field
from mitosheet.data_in_mito import DataTypeInMito, get_data_type_in_mito
from mitosheet.mito_analytics import log
from mitosheet.user import (
    UJ_INTENDED_BEHAVIOR, UJ_USER_EMAIL, UJ_RECEIVED_TOURS
)

class WidgetStateContainer():
    """
    Holds the state of the steps, which represents operations that
    have been performed on the input dataframes. 
    """

    def __init__(self, args):
        """
        When initalizing the Widget State Container, we also do preprocessing
        of the arguments that were passed to the mitosheet. 

        All preprocessing can be found in mitosheet/preprocessing, and each of 
        the transformations are applied before the data is considered imported.
        """
        # We just randomly generate analysis names. 
        # We append a UUID to note that this is not an analysis the user has saved.
        self.analysis_name = 'UUID-' + str(uuid.uuid4())

        # The args are a tuple of dataframes or strings, and we start by making them
        # into a list, and making copies of them for safe keeping
        self.original_args = [
            arg.copy(deep=True) if isinstance(arg, pd.DataFrame) else deepcopy(arg) for arg in args
        ]

        # Then, we go through the process of actually preprocessing the args
        for PREPROCESS_STEP in PREPROCESS_STEPS:
            args = PREPROCESS_STEP['execute'](args)

        # Then we initialize the first initalize step
        self.steps = []
        # We display the state that exists after the curr_step_idx is applied,
        # which means you can never see before the initalize step
        self.curr_step_idx = 0

        self.data_type_in_mito: DataTypeInMito = get_data_type_in_mito()

        execute_initialize_step(self, args)

    @property
    def curr_step(self):
        """
        Returns the current step object as a property of the object,
        so reference it with self.curr_step
        """
        return self.steps[self.curr_step_idx]

    @property
    def num_sheets(self):
        """
        Duh. :)
        """
        return len(self.steps[self.curr_step_idx]['dfs'])

    @property
    def dfs(self) -> List[pd.DataFrame]:
        return self.steps[self.curr_step_idx]['dfs']

    @property
    def df_names_json(self):
        """
        A JSON object containing the names of the dataframes
        """
        return json.dumps({'df_names': self.curr_step['df_names']})

    @property
    def sheet_json(self):
        """
        sheet_json contains a serialized representation of the data
        frames that is then fed into the ag-grid in the front-end. 

        NOTE: we only display the _first_ 2,000 rows of the dataframe
        for speed reasons. This results in way less data getting 
        passed around
        """
        return dfs_to_json(self.curr_step['dfs'])
    
    @property
    def df_shape_json(self):
        """
        Returns the df shape (rows, columns) of each dataframe in the 
        current step!
        """
        return json.dumps([
            {'rows': df.shape[0], 'cols': df.shape[1]}
            for df in self.curr_step['dfs']
        ])

    @property
    def column_spreadsheet_code_json(self):
        """
        column_spreadsheet_code_json is a list of all the spreadsheet
        formulas that users have used, for each sheet they have. 
        """
        return json.dumps(self.curr_step['column_spreadsheet_code'])

    @property
    def code_json(self):
        """
        This code json string is sent to the front-end and is what
        ends up getting displayed in the codeblock. 
        """
        return json.dumps(transpile(self))

    @property
    def column_filters_json(self):
        """
        This column_filters list is used by the front end to display
        the filtered icons in the UI
        """
        return json.dumps(self.curr_step['column_filters'])
    
    @property
    def column_type_json(self):
        """
        Returns a list of JSON objects that hold the type of each
        data in each column.
        """
        return json.dumps(self.curr_step['column_type'])

    @property
    def user_email(self):
        """
        Returns the user_email from user.json
        """
        return get_user_field(UJ_USER_EMAIL)

    @property
    def received_tours(self):
        """
        Returns the tours that the user has received
        """
        return json.dumps(get_user_field(UJ_RECEIVED_TOURS))

    @property
    def intended_behavior(self):
        """
        Returns the intended_behavior of the user as inputted in the signup flow
        """
        return json.dumps(get_user_field(UJ_INTENDED_BEHAVIOR))

    @property
    def step_data_list_json(self):
        """
        Returns a list of step data
        """
        step_data_list = []
        for index, step in enumerate(self.steps):
            STEP_OBJ = STEP_TYPE_TO_STEP[step['step_type']]
            params = {key: value for key, value in step.items() if key in STEP_OBJ['params']}
            step_data_list.append({
                'step_id': step['step_id'],
                'step_idx': index,
                'step_type': step['step_type'],
                'step_display_name': STEP_OBJ['step_display_name'],
                'step_description': STEP_OBJ['describe'](
                    df_names=step['df_names'],
                    **params,
                )
            })

        return json.dumps(step_data_list)

    def edit_event_should_overwrite_curr_step(self, edit_event):
        """
        We overwrite the step if the step_ids are shared between the curr step
        and the edit event, or if if it is an set formula event that is setting 
        the formula of a column that was updated the last step
        """
        overwrite_formula_step = self.curr_step['step_type'] == SET_COLUMN_FORMULA_STEP_TYPE \
                and edit_event['type'] == SET_COLUMN_FORMULA_EVENT \
                and self.curr_step['sheet_index'] == edit_event['sheet_index'] \
                and self.curr_step['column_header'] == edit_event['column_header']

        return self.curr_step['step_id'] == edit_event['step_id'] or overwrite_formula_step

    def handle_edit_event(self, edit_event):
        """
        Updates the widget state with a new step that was created
        by the edit_event. Each edit_event creates at most one step. 

        If there is an error in the creation of the new step, this
        function will delete the new, invalid step.
        """
        # NOTE: We ignore any edit if we are in a historical state, for now. This is a result
        # of the fact that we don't allow previous editing currently
        if self.curr_step_idx != len(self.steps) - 1:
            return

        try:
            curr_step = self.steps[-1]

            overwrite = self.edit_event_should_overwrite_curr_step(edit_event)

            if overwrite:
                # If we are overwriting the event, then we set the current
                # step back 1 from the actual current step, so that we start
                # from the correct state
                curr_step = self.steps[-2]             

            step_obj = EVENT_TYPE_TO_STEP[edit_event['type']]

            # Saturate the event
            if step_obj['saturate'] is not None:
                step_obj['saturate'](curr_step, edit_event)

            # Get the params for this event
            params = {key: value for key, value in edit_event.items() if key in step_obj['params']}
            # If it's filter, we need to do a lot of extra work
            # so we sent it into the execute function directly
            if step_obj['step_type'] == 'filter_column':
                execute_filter_column(
                    self,
                    **params
                )
                self.curr_step_idx = len(self.steps) - 1
                # If we made a new step, save the step id of this step
                if 'step_id' not in self.curr_step:
                    self.curr_step['step_id'] = edit_event['step_id']
                return 

            # If the user performs a simple import, update the wsc with 
            # whether they used personal data or not. 
            if step_obj['step_type'] == 'simple_import':
                data_type_in_mito = get_data_type_in_mito(*params['file_names'])

                # If they imported PERSONAL data, set type_of_data_in_mito to personal & log PERSONAL data
                if data_type_in_mito == DataTypeInMito.PERSONAL:
                    log('used_personal_data')
                    self.data_type_in_mito = DataTypeInMito.PERSONAL

                # If they imported TUTORIAL data, and they didn't already import PERSONAL data, set type_of_data_in_mito to TUTORIAL
                if data_type_in_mito == DataTypeInMito.TUTORIAL and not self.data_type_in_mito == DataTypeInMito.PERSONAL:
                    self.data_type_in_mito = DataTypeInMito.TUTORIAL

                # If they imported PROVIDED data, and they didn't already import PERSONAL or TUTORIAL data, 
                # set type_of_data_in_mito to PROVIDED
                if (
                    data_type_in_mito == DataTypeInMito.PROVIDED and 
                    not self.data_type_in_mito == DataTypeInMito.PERSONAL and 
                    not self.data_type_in_mito == DataTypeInMito.TUTORIAL
                ):
                    self.data_type_in_mito = DataTypeInMito.PROVIDED

                            
            # Actually get the new step
            new_step = step_obj['execute'](curr_step, **params)

            # If the new step is None, we dont do anything with it, otherwise we
            # add it to the steps
            if new_step is not None:
                # Save the parameters in the new step
                for key, value in params.items():
                    new_step[key] = value
                
                # Furthermore, we save the step_id
                new_step['step_id'] = edit_event['step_id']

                # Finially, we append this step in the correct location to the steps
                if not overwrite:
                    self.steps.append(new_step)
                else:
                    self.steps[-1] = new_step
            
            # and then update the index of the current step
            self.curr_step_idx = len(self.steps) - 1
        except:

            # We bubble the error up if it occurs
            # https://stackoverflow.com/questions/6593922/letting-an-exception-to-bubble-up
            raise


    def handle_update_event(self, update_event):
        """
        Handles any event that isn't caused by an edit, but instead
        other types of new data coming from the frontend (e.g. the df names 
        or some existing steps).
        """
        for update in UPDATES:
            if update_event['type'] == update['event_type']:
                # Get the params for this event
                params = {key: value for key, value in update_event.items() if key in update['params']}
                # Actually execute this event
                update['execute'](self, **params)
                # And then return
                return

        raise Exception(f'{update_event} is not an update event!') 

    def rerun_steps_from_index(self, index=None, new_steps=None):
        """
        Reruns steps starting from the given index. If no index is given
        then does not run any of the existing steps. 

        If new_steps are given, then will run these as well. If no new_steps
        are given then will not run them. 

        Note that as all that is needed for replay is the step summaries,
        and so new_steps may be something passed from a read in analysis
        """
        if index is None:
            # If no index is given, then we run from the last step, but make
            # sure to not rerun the initalization step (as it should only ever
            # run once
            index = max(len(self.steps) - 1, 1)

        steps_to_replay = self.steps[index:]
        # If there are new steps, we "replay" them as well
        if new_steps is not None:
            steps_to_replay.extend(new_steps)

        # We make a shallow copy of the steps, as none of the objects
        # will be changed by the step summaries we apply   
        old_steps = copy(self.steps)

        # Then, we delete anything after the index we're replaying from
        self.steps = self.steps[:index]

        try:
            for step in steps_to_replay:

                curr_step = self.steps[-1]

                step_type = step['step_type']

                step_obj = STEP_TYPE_TO_STEP[step_type]

                # Get the params for this event
                params = {key: value for key, value in step.items() if key in step_obj['params']}

                # If it's filter, we need to do a lot of extra work
                # so we sent it into the execute function directly
                if step_obj['step_type'] == 'filter_column':
                    execute_filter_column(
                        self,
                        **params
                    )
                    self.curr_step_idx = len(self.steps) - 1
                    # We always make a new step, so we also save the id of this step
                    self.curr_step['step_id'] = get_new_id()
                    continue 


                # Actually execute this event
                new_step = step_obj['execute'](curr_step, **params)
                
                # Save the params for this event
                for key, value in params.items():
                    new_step[key] = value

                # Every step also needs an id, which we add
                new_step['step_id'] = get_new_id()

                self.steps.append(new_step)
                self.curr_step_idx = len(self.steps) - 1

        except Exception as e:
            print(e)
            # We remove all applied steps if there was an error
            self.steps = old_steps
            self.curr_step_idx = len(old_steps) - 1

            # And report a generic error to the user
            raise make_execution_error()