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

import sys
import json
import logging
import re
from copy import deepcopy
from os import listdir
from os.path import isfile, join
from ConfigParser import SafeConfigParser
import codecs

__logger__ = logging.getLogger(__name__)

# Loaded configuration. Module variable with all loaded properties: JSON
config = None

# Loaded language properties: ConfigParser
language_props = None


def load_project_properties(json_file):
    """
    Parses the JSON configuration file located in the conf folder and
    stores the resulting dictionary in the config global variable.
    :param: (json_file) Path to properties file to be loaded.
    """

    __logger__.info("Loading project properties from %s", json_file)
    try:
        with open(json_file) as config_file:
            try:
                global config
                config = json.load(config_file)
            except Exception, e:
                __logger__.error('Error parsing config file: %s' % e)
                sys.exit(1)
    except IOError, e:
        __logger__.error('%s properties file CANNOT be opened: %s', json_file, e)

    __logger__.debug("Properties loaded: %s", config)


def load_lang_properties(lang, lang_dir):
    """
    Loads all lang properties for the files located in the given lang_dir. The files to load will be the
     ones that match with the given language. File format to load: <lang>_*.*.
    :param lang: (string) Language of the file to load the properties from
    :param lang_dir: (string) Dir where the lang files are located
    :return: None. The loaded lang properties will be saved in the global var of this file: language_props
    """

    __logger__.info("Loading all language files from '%s'. Language: '%s'", lang_dir, lang)
    file_list = [join(lang_dir, f) for f in listdir(lang_dir) if isfile(join(lang_dir, f)) and
                 f.startswith("{}_".format(lang))]
    __logger__.debug("Language properties file list: '%s'", file_list)

    global language_props

    language_props = SafeConfigParser()
    for file in file_list:
        # Open the file with the correct encoding
        with codecs.open(file, 'r', encoding='utf-8') as f:
            language_props.readfp(f)
    __logger__.debug("Language properties loaded for: '%s'", language_props.sections())


def get_values_of_lang_section(section):
    """
    Returns a list with all the values (only values without key) of the given section for the
     loaded language properties file.
    :param section: (string) Name of the section.
    :return: (list) List with all the values of the given section for the loaded language properties
    """

    value_list = list()
    for key, value in language_props.items(section):
        value_list.append(value)

    return value_list


def _is_property_in_config(param):
    """
    Checks if the given param should be loaded from Environment Configuration File
    Format: [CONF:services.vamps.user]
    :param param: Parameter to check its value.
    :return: returning a match object, or None if no match was found.
    """

    return re.match("\[CONF:(.*)\]", param)


def map_config_param(param_value, config_json=None):
    """
    Analyzes the given parameter value and find out its real value into the loaded environment configuration file.
    :param param_value: Parameter value. If it should be replaced by its real value into configuration file, when
    the format is something like this: [CONF:services.vamps.user], when I want to access to these properties:
        {
          "services":{
            "vamps":{
              "user": "cyber-sec-user@11paths.com",
              "password": "MyPassword"
            }
          }
        }
    :param config_json: (dict) Loaded configuration file (environment properties)
    :return: Real parameter value. In this case, the string "cyber-sec-user@11paths.com". It the param value
    does not suit this format, the returned param value is the same as the given one.
    """

    if not config_json:
        config_json = config

    match_group = _is_property_in_config(param_value)
    if match_group:
        properties_list = match_group.group(1).split(".")
        aux_config_json = deepcopy(config_json)
        try:
            for property in properties_list:
                aux_config_json = aux_config_json[property]

            __logger__.info("Mapping param '%s' to its configured value '%s'", param_value, aux_config_json)
        except KeyError as e:
            __logger__.error("Mapping chain not found in the configuration properties file")
            raise e
        return aux_config_json
    else:
        return param_value
