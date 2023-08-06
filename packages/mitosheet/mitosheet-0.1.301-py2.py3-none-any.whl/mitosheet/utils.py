#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains helpful utility functions
"""
from copy import deepcopy
import json
from mitosheet.sheet_functions.types.utils import get_datetime_columns, get_float_columns, get_mito_type, get_timedelta_columns
import pandas as pd
import numpy as np
import numbers
from string import ascii_letters, digits
import subprocess
import os
import uuid
import re

def make_valid_header(column_header):
    """
    Takes a header, and performs replaces against common characters
    to make the column_header valid!
    """
    # If it's just numbers, turn it into a string (with an underscore)
    if isinstance(column_header, numbers.Number):
        return str(column_header).replace('.', '_') + '_'

    # If it's just numbers in a string, add an underscore
    if column_header.isdigit():
        return column_header + "_"

    # Replace common invalid seperators with valid seperators
    replace_dict = {
        ' ': '_',
        '-': '_',
        '(': '_',
        ')': '_',
        '/': '_',
        '#': 'num',
        ',': '_',
        '.': '_',
        '!': '_',
        '?': '_'
    }
    for find, replace in replace_dict.items():
        column_header = column_header.replace(find, replace)
    
    if not is_valid_header(column_header):
        # Because we detect column headers using a word match, any word character counts
        # in a valid character
        pattern = re.compile("\w")

        new_header = ''.join([
            c for c in column_header if pattern.search(c)
        ])
        if not is_valid_header(new_header):
            # And then append an underscore, for good measure, and this should fix it!
            new_header = new_header + '_'

        return new_header
    return column_header

def is_valid_header(column_header):
    """
    A header is valid if It is a string that is made up of all word characters,
    with at least one non numeric char, and has at least one char.

    Valid examples: A, ABC, 012B, 213_bac, 123_123
    Invalid examples: 123, 123!!!, ABC!, 123-123

    This is a result of not being able to distingush column headers from constants
    otherwise, and would not be necessary if we had a column identifier!
    """
    
    # Note the start and end characters in the regex, to make sure it's a full match
    return isinstance(column_header, str) and \
        len(column_header) > 0 and \
        re.compile("^\w+$").search(column_header) and \
        not column_header.isdigit()


def get_invalid_headers(df: pd.DataFrame):
    """
    Given a dataframe, returns a list of all the invalid headers this list has. 
    """
    return [
        header for header in df.columns.tolist()
        if not is_valid_header(header)
    ]

def get_header_renames(column_headers):
    """
    Given a list of column headers, returns a mapping from old, invalid headers to
    new, valid headers. Empty if no renames are necessary.
    """
    renames = dict()
    for column_header in column_headers:
        if not is_valid_header(column_header):
            valid_header = make_valid_header(column_header)
            renames[column_header] = valid_header

    return renames


def dfs_to_json(dfs):
    return json.dumps([df_to_json_dumpsable(df) for df in dfs])


def df_to_json_dumpsable(df: pd.DataFrame):
    """
    Returns a dataframe represented in a way that can be turned into a 
    JSON object with json.dumps
    """
    # First, we get the head, and then we make a copy (as we modify the df below)
    # NOTE: we get the head first for efficiency reasons.
    df = df.head(n=2000).copy(deep=True) # we only show the first 2k rows!
    
    # Second, we figure out which of the columns contain dates, and we
    # convert them to string columns (for formatting reasons).
    # NOTE: we don't use date_format='iso' in df.to_json call as it appends seconds to the object, 
    # see here: https://stackoverflow.com/questions/52730953/pandas-to-json-output-date-format-in-specific-form
    date_columns = get_datetime_columns(df)
    for column_header in date_columns:
        df[column_header] = df[column_header].dt.strftime('%Y-%m-%d %X')

    # Third, we figure out which of the columns contain timedeltas, and 
    # we format the timedeltas as strings to make them readable
    timedelta_columns = get_timedelta_columns(df)
    for column_header in timedelta_columns:
        df[column_header] = df[column_header].apply(lambda x: str(x))

    # Then, we get all the float columns and actually make them 
    # look like floating point values, by converting them to strings
    float_columns = get_float_columns(df)
    for column_header in float_columns:
        # Convert the value to a string if it is a number, but leave it alone if its a NaN 
        # as to preserve the formatting of NaN values. 
        df[column_header] = df[column_header].apply(lambda x: x if np.isnan(x) else str(x))

    json_obj = json.loads(df.to_json(orient="split"))
    # Then, we go through and find all the null values (which are infinities),
    # and set them to 'NaN' for display in the frontend.
    for d in json_obj['data']:
        for idx, e in enumerate(d):
            if e is None:
                d[idx] = 'NaN'

    return json_obj


def does_sheet_index_exist_within_step(step, sheet_index):
    """
    Returns true iff a sheet_index exists within a step
    """
    return not (sheet_index < 0 or sheet_index >= len(step['dfs']))


def add_df_to_step(step, new_df, df_name=None):
    """
    Helper function for adding a new dataframe to the current step!
    """
    # Update dfs by appending new df
    step['dfs'].append(new_df)
    # Also update the dataframe name
    if df_name is None:
        step['df_names'].append(f'df{len(step["df_names"]) + 1}')
    else:
        step['df_names'].append(df_name)
    
    # Update all the variables that depend on column_headers
    column_headers = new_df.keys()
    step['column_metatype'].append({column_header: 'value' for column_header in column_headers})
    step['column_type'].append({column_header: get_mito_type(new_df[column_header]) for column_header in column_headers})
    step['column_spreadsheet_code'].append({column_header: '' for column_header in column_headers})
    step['column_python_code'].append({column_header: '' for column_header in column_headers})
    step['column_evaluation_graph'].append({column_header: set() for column_header in column_headers})
    step['column_filters'].append({column_header: {'operator':'And', 'filters': []} for column_header in column_headers})

def create_new_step(prev_step, step_type, deep=True):
    """
    Creates a new step with new_step_id and step_type that starts
    with the ending state of the previous step

    We default to deep=True, which makes a deep copy of the dataframes
    that are in the previous step. However, for steps that don't modify
    any existing dataframes (e.g. imports, merges, pivots), we can 
    set this to deep=False/
    """
    # The new step is a copy of the previous step, where we only take the data we need
    # (which is the formula content only)
    new_step = dict()

    new_step['step_type'] = step_type
    new_step['column_metatype'] = deepcopy(prev_step['column_metatype'])
    new_step['column_type'] = deepcopy(prev_step['column_type'])
    new_step['column_spreadsheet_code'] = deepcopy(prev_step['column_spreadsheet_code'])
    new_step['column_python_code'] = deepcopy(prev_step['column_python_code'])
    new_step['column_evaluation_graph'] = deepcopy(prev_step['column_evaluation_graph'])
    new_step['column_filters'] = deepcopy(prev_step['column_filters'])
    new_step['dfs'] = [df.copy(deep=deep) for df in prev_step['dfs']]
    new_step['df_names'] = deepcopy(prev_step['df_names'])

    return new_step


def get_random_id():
    """
    Creates a new random ID for the user, which for any given user,
    should only happen once.
    """
    return str(uuid.uuid1())

def get_new_id():
    return str(uuid.uuid4())


