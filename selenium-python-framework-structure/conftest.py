"""
Funciones basicas del Framework
"""

import os
import pathlib

import pytest

from utils import driver_config
from utils.driver_config import get_driver_instance, quit_driver, init_driver


def pytest_addoption(parser):
    parser.addoption('--env', action='store', default='test', help='select environments')
    parser.addoption('--role', action='store', default='', help='"ci" to used role based auth')

    parser.addoption('--browser', action='store', default='none',
                     help="supported browser: chrome, firefox, appium, browserstack")
    parser.addoption('--headless', action='store', default='none', help='true/false to use or not headless mode')
    parser.addoption('--maximized', action='store', default='none', help='true/false to maximize browser')
    parser.addoption('--device_name', action='store', default='none',
                     help='device name to execute using mobile emulation in Chrome')

    parser.addoption('--bs_browser', action='store', default='none', help='browser name to use on BrowserStack')
    parser.addoption('--bs_browser_version', action='store', default='none', help='browser version to use on BS')
    parser.addoption('--bs_os', action='store', default='none', help='OS to run test on BS')

    parser.addoption('--device', action='store', default='none', help='device name to use on BS for mobile browser')
    parser.addoption('--browserName', action='store', default='none', help='use android or ios to run tests on BS')

    parser.addoption('--os_version', action='store', default='none', help='for desktop or mobile execution on BS')


def pytest_configure(config):
    os.environ["env"] = config.getoption('env')
    os.environ["role"] = config.getoption('role')

    os.environ["browser"] = config.getoption('browser')
    os.environ["headless"] = config.getoption('headless')
    os.environ["maximized"] = config.getoption('maximized')
    os.environ["device_name"] = config.getoption('device_name')

    os.environ["bs_browser"] = config.getoption('bs_browser')
    os.environ["bs_browser_version"] = config.getoption('bs_browser_version')
    os.environ["bs_os"] = config.getoption('bs_os')

    os.environ["device"] = config.getoption('device')
    os.environ["browserName"] = config.getoption('browserName')

    os.environ["os_version"] = config.getoption('os_version')

    driver_config.set_driver_type()


@pytest.fixture
def driver():
    # Init driver
    init_driver()
    # Get current driver instance
    yield get_driver_instance()
    # For cleanup, quit the driver
    quit_driver()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            method_name = report.nodeid.split('/')
            method_name = method_name[len(method_name) - 1].replace("::", "_") + ".png"
            file_path = str(pathlib.Path(__file__).parent) + '/report/images/' + method_name
            _capture_screenshot(file_path)
            file_name = 'images/' + method_name
            if file_path:
                html = f'<div><img src="{file_name}" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>'
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name):
    try:
        get_driver_instance().get_screenshot_as_file(name)
    except:
        pass


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed ({})".format(previousfailed.name))