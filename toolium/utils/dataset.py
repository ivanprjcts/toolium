# -*- coding: utf-8 -*-
u"""
Copyright (c) 2016 Telefonica Digital | ElevenPaths

This file is part of Toolium.

icensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json

"""
Original file from Telefónica I+D:
    https://github.com/telefonicaid/lettuce-tools/blob/master/lettuce_tools/dataset_utils/dataset_utils.py

dataset_utils module contains:
    - A dataset manager to prepare test data:
        * generate_fixed_length_params: Transforms the '[LENGTH]' param value to a valid length.
        * remove_missing_params: Remove parameters with value '[MISSING]'
        * infere_datatypes: Inferes type of parameters to convert them in the suitable var type
"""

__author__ = "Telefónica I+D, qateam@11paths.com"
__copyright__ = "Copyright 2015"
__license__ = " Apache License, Version 2.0"


def prepare_data(data):
    """
    Generate a fixed length data for elements tagged with the text [LENGTH]
    Removes al the data elements tagged with the text [MISSING_PARAM]
    Transformes data from string to primitive type
    :param data: hash entry
    :return cleaned data
    """
    try:
        data = generate_fixed_length_params(data)
        data = remove_missing_params(data)
        data = infere_datatypes(data)
        return data
    except:
        return None


def prepare_param(param):
    """
    Generate a fixed length data for elements tagged with the text [LENGTH]
    None for params tagged with the text [MISSING_PARAM]
    Empty string for params tagged with the text [EMPTY]
    :param param: Test parameter
    :return data with the correct replacements
    """

    if "[MISSING_PARAM]" in param:
        new_param = None
    elif "[EMPTY]" in param:
        new_param = ""
    else:
        new_param = generate_fixed_length_param(param)

    return infere_datatypes(new_param)


def remove_missing_params(data):
    """
    Removes all the data elements tagged with the text [MISSING_PARAM]
    :param data: Lettuce step hash entry
    :return data without not desired params
    """
    try:
        for item in data.keys():
            if "[MISSING_PARAM]" in data[item]:
                del(data[item])
    finally:
        return data


def generate_fixed_length_param(param):
    """
    Generate a fixed length param if the elements matches the expression
    [<type>_WITH_LENGTH_<length>]. E.g.: [STRING_WITH_LENGTH_15]
    :param param: Lettuce param
    :return param with the desired length
    """
    try:
        if "_WITH_LENGTH_" in param:
            if "_ARRAY_WITH_LENGTH_" in param:
                seeds = {'STRING': 'a', 'INTEGER': 1}
                seed, length = param[1:-1].split("_ARRAY_WITH_LENGTH_")
                param = list(seeds[seed] for x in xrange(int(length)))
            elif "JSON_WITH_LENGTH_" in param:
                length = int(param[1:-1].split("JSON_WITH_LENGTH_")[1])
                param = dict((str(x), str(x)) for x in xrange(length))
            else:
                seeds = {'STRING': 'a', 'INTEGER': "1"}
                # The chain to be generated can be just a part of param
                start = param.find("[")
                end = param.find("]")
                seed, length = param[start + 1:end].split("_WITH_LENGTH_")
                generated_part = seeds[seed] * int(length)
                placeholder = "[" + seed + "_WITH_LENGTH_" + length + "]"
                param = param.replace(placeholder, generated_part)
                if seed is "INTEGER":
                    param = int(param)
    finally:
        return param


def generate_fixed_length_params(data):
    """
    Generate a fixed length data for the elements that match the expression
    [<type>_WITH_LENGTH_<length>]. E.g.: [STRING_WITH_LENTGH_15]
    :param data: hash entry
    :return data with the desired params with the desired length
    """
    try:
        for item in data.keys():
            data[item] = generate_fixed_length_param(data[item])
    finally:
        return data


def infere_datatypes(data):
    """
    Process the input data and replace the values in string format with the
    the appropriate primitive type, based on its content
    :param data: list of items, dict of items or single item
    :return processed list of items, dict of items or single item
    """

    """ Separate the process of lists, dicts and plain items"""
    try:

        if isinstance(data, dict):  # dict of items
            for key in data:
                data[key] = _get_item_with_type(data[key])

        elif isinstance(data, list):  # list of items
            for index in range(len(data)):
                data[index] = _get_item_with_type(data[index])

        else:  # single item
            data = _get_item_with_type(data)
    finally:
        return data


def _get_item_with_type(data):
    """
    Transform data from string to primitive type
    :param data: Data to be transformed
    :return data with the correct type
    """
    if "[TRUE]" in data:  # boolean
        data = True
    elif "[FALSE]" in data:  # boolean
        data = False
    elif data.startswith("{") and data.endswith("}"):  # json
        data = json.loads(data)
    else:
        try:  # maybe an int
            data = int(data)
        except:
            try:  # maybe a float
                data = float(data)
            except:
                pass  # if no condition matches, leave the data unchanged
    return data
