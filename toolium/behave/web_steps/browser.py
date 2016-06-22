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

import logging
from behave import step
from toolium.driver_wrappers_pool import DriverWrappersPool

__logger__ = logging.getLogger(__name__)


@step(u'I set up browser width to "{width}" and height to "{height}"')
def set_up_browser_size(context, width, height):
    DriverWrappersPool.get_default_wrapper().driver.set_window_size(int(width), int(height))


@step(u'I go back to previous page')
def go_back_previous_page(context):
    DriverWrappersPool.get_default_wrapper().driver.execute_script("window.history.go(-1)")


@step(u'I refresh browser')
def go_back_previous_page(context):
    DriverWrappersPool.get_default_wrapper().driver.refresh()


@step(u'I delete cookies')
def delete_cookies(context):
    driver_wrapper = DriverWrappersPool.get_default_wrapper()
    cookies = driver_wrapper.driver.get_cookies()

    __logger__.info("Cookies list: %s", cookies)

    try:
        context.page.driver.delete_all_cookies()
    except:
        __logger__.warn("No cookies deleted")


@step(u'I get cookies')
def get_cookies(context):
    driver_wrapper = DriverWrappersPool.get_default_wrapper()
    context.cookies = driver_wrapper.driver.get_cookies()
