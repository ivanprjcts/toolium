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

from toolium.pageobjects.page_object import PageObject

__author__ = "ElevenPaths QA Team <qateam@11paths.com>"


class PageObjectAutoloaded(PageObject):
    """
    Class to represent a web page or a mobile application screen when it is auto-loaded
    from a specification file (YAML) dynamically in runtime. All its elements will be
    auto-created based on this specification.

    :type name: (string) Name to identify the auto-loaded PageObject. e.i: LoginPage
    """

    def __init__(self, driver_wrapper=None):
        """Initialize page object properties and update their page elements

        :param driver_wrapper: driver wrapper instance
        """

        super(PageObjectAutoloaded, self).__init__(driver_wrapper=driver_wrapper)

        # Name to identify the auto-loaded PageObject.
        self.name = None

    def wait_until_loaded(self, timeout=10):
        """
        Wait until page is loaded using the auto-loaded information.
        :param timeout: max time to wait
        :returns: this page object instance
        """

        for page_element in super(PageObjectAutoloaded, self)._get_page_elements():
            if page_element.if_wait:
                self.logger.debug("Waiting for element loaded: %s", page_element)
                page_element.wait_until_visible(timeout=timeout)

        return self
