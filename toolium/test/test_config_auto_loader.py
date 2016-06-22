# -*- coding: utf-8 -*-
u"""
Copyright (c) 2016 Telefonica Digital | ElevenPaths | qateam@11paths.com

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

import unittest
from nose.tools import assert_true, assert_equal, assert_in

from toolium.config_auto_loader import add_attributes_to_page_object, _init_logger, \
    create_page_objects, load_page_object_definition, get_page_object
from toolium.pageobjects.page_object_autoloaded import PageObjectAutoloaded
from selenium.webdriver.common.by import By


class TestConfigAutoLoader(unittest.TestCase):

    YAML_FILE_DEFINITION = "resources/page_object_definition.yaml"

    @classmethod
    def setUpClass(cls):
        _init_logger()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add_attributes_to_page_object(self):

        page_element = \
            {
                "Text": {
                    "Name": "element1",
                    "Locator-Type": "ID",
                    "Locator-Value": "LOCATOR-VALUE1",
                    "Wait-For-Loaded": True
                }
            }

        page_object = PageObjectAutoloaded()
        add_attributes_to_page_object(page_element, page_object)

        assert_true(hasattr(page_object, "element_element1"))
        assert_true(hasattr(page_object.element_element1, "if_wait"))
        assert_equal(page_object.element_element1.locator, (By.ID, "LOCATOR-VALUE1"))
        assert_equal(page_object.element_element1.if_wait, True)

    def test_add_attributes_to_page_object_no_wait(self):

        page_element = \
            {
                "InputText": {
                    "Name": "element2",
                    "Locator-Type": "XPATH",
                    "Locator-Value": "LOCATOR-VALUE2"
                }
            }

        page_object = PageObjectAutoloaded()
        add_attributes_to_page_object(page_element, page_object)

        assert_true(hasattr(page_object, "element_element2"))
        assert_true(hasattr(page_object.element_element2, "if_wait"))
        assert_equal(page_object.element_element2.locator, (By.XPATH, "LOCATOR-VALUE2"))
        assert_equal(page_object.element_element2.if_wait, False)

    def test_init_page_objects(self):

        page_element_list_object1 = \
            [
                {
                    "Text": {
                        "Name": "element1",
                        "Locator-Type": "ID",
                        "Locator-Value": "LOCATOR-VALUE1",
                        "Wait-For-Loaded": True
                    }
                },
                {
                    "InputText": {
                        "Name": "element2",
                        "Locator-Type": "XPATH",
                        "Locator-Value": "LOCATOR-VALUE2",
                        "Wait-For-Loaded": False
                    }
                }
            ]

        page_element_list_object2 = \
            [{
                "Button": {
                    "Name": "element3",
                    "Locator-Type": "ID",
                    "Locator-Value": "LOCATOR-VALUE3"
                }
            }]

        page_definition_data = \
            {
                "LoginPage": page_element_list_object1,
                "DashboardPage": page_element_list_object2
            }

        page_objects_loaded = create_page_objects(page_definition_data)

        assert_true(hasattr(page_objects_loaded[0], "name"))
        assert_true(hasattr(page_objects_loaded[1], "name"))

        assert_equal(page_objects_loaded[0].name, "DashboardPage")
        assert_equal(page_objects_loaded[1].name, "LoginPage")

        assert_true(hasattr(page_objects_loaded[0], "element_element3"))
        assert_true(hasattr(page_objects_loaded[1], "element_element1"))
        assert_true(hasattr(page_objects_loaded[1], "element_element2"))

    def test_load_page_object_definition(self):
        page_definition_data = load_page_object_definition(self.YAML_FILE_DEFINITION)

        assert_in("Login", page_definition_data)
        assert_in("Dashboard", page_definition_data)
        assert_in("Profile", page_definition_data)

        assert_in("Text", page_definition_data["Login"][0])
        assert_in("InputText", page_definition_data["Login"][1])
        assert_in("InputText", page_definition_data["Login"][2])
        assert_in("Button", page_definition_data["Dashboard"][0])
        assert_in("InputText", page_definition_data["Profile"][0])

    def test_load_and_init_page_objects(self):
        page_definition_data = load_page_object_definition(self.YAML_FILE_DEFINITION)
        page_objects_loaded = create_page_objects(page_definition_data)

        assert_true(hasattr(page_objects_loaded[0], "name"))
        assert_true(hasattr(page_objects_loaded[1], "name"))
        assert_true(hasattr(page_objects_loaded[2], "name"))

        assert_equal(page_objects_loaded[2].name, "Dashboard")
        assert_equal(page_objects_loaded[1].name, "Login")
        assert_equal(page_objects_loaded[0].name, "Profile")

        assert_true(hasattr(page_objects_loaded[1], "element_form"))
        assert_true(hasattr(page_objects_loaded[1], "element_username"))
        assert_true(hasattr(page_objects_loaded[1], "element_password"))

        assert_true(hasattr(page_objects_loaded[2], "element_logout"))

        assert_true(hasattr(page_objects_loaded[0], "element_name"))

    def test_get_page_object(self):
        page_definition_data = load_page_object_definition(self.YAML_FILE_DEFINITION)
        page_objects_loaded = create_page_objects(page_definition_data)

        login_page = get_page_object(page_objects_loaded, "Login")

        assert_true(hasattr(login_page, "element_form"))
        assert_true(hasattr(login_page, "element_username"))
        assert_true(hasattr(login_page, "element_password"))
        assert_true(hasattr(login_page, "element_form"))

        assert_equal(login_page.name, "Login")
