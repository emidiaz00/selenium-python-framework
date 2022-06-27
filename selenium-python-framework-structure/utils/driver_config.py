import os
from distutils import util

from appium import webdriver as appium_web_driver
from selenium import webdriver as selenium_web_driver
from selenium.webdriver import Chrome, Firefox
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.microsoft import IEDriverManager

from utils.config_loader import read_config_file, read_config_file_with_validation

DEFAULT_WAIT_TIME = 10
SUPPORTED_BROWSERS = ['chrome', 'firefox', 'safari', 'appium', 'browserstack', 'ie', 'edge']
driver_instance = None


def config_browser():
    browser = os.environ["browser"] if os.environ["browser"] != 'none' else read_config_file("driver", 'browser')
    if browser not in SUPPORTED_BROWSERS:
        raise Exception(f'"{browser}" is not a supported browser')
    return browser


def config_implicit_timeout():
    try:
        return int(read_config_file("driver", 'implicit_timeout'))
    except:
        return wDEFAULT_WAIT_TIME


def config_explicit_timeout():
    try:
        return int(read_config_file("driver", 'explicit_timeout'))
    except:
        return DEFAULT_WAIT_TIME


def get_driver_instance():
    global driver_instance
    if driver_instance is None:
        raise Exception("Can't get a driver instance. Reason: No driver instantiated.")
    return driver_instance


def quit_driver():
    global driver_instance
    if driver_instance is None:
        raise Exception("Can't quit driver. Reason: No driver instantiated.")
    driver_instance.quit()
    driver_instance = None


def init_driver():
    global driver_instance
    if driver_instance is None:
        browser = config_browser()
        # Initialize WebDriver
        if os.environ["headless"] != 'none':
            headless = util.strtobool(os.environ["headless"])
        else:
            headless = read_config_file("driver", 'headless')

        if os.environ["maximized"] != 'none':
            maximized = util.strtobool(os.environ["maximized"])
        else:
            maximized = read_config_file("driver", 'maximized')

        if browser == 'chrome':
            chrome_options = selenium_web_driver.ChromeOptions()
            chrome_options.add_argument('ignore-certificate-errors')
            chrome_options.add_argument("--incognito")
            """path1 = ".." #\\test\\pdf_POL264
            start = __file__
            path = os.path.dirname(os.path.relpath(path1, start))
            dirname = os.path.dirname(f"..\\{__file__}")
            filename = os.path.join(dirname, '\\test\\pdf_POL264')
            prefs = {"download.default_directory" : filename}
            chrome_options.add_experimental_option("prefs", prefs)"""
            if headless:
                chrome_options.add_argument('--headless')

            try:  # If a device name is added into driver config, mobile emulation is activated
                device_name = os.environ["device_name"] if os.environ["device_name"] != 'none' else read_config_file(
                    "driver", 'device_name')
                mobile_emulation = {"deviceName": device_name}
                chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
            except:
                pass

            driver_instance = Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        elif browser == 'firefox':
            driver_instance = Firefox(executable_path=GeckoDriverManager().install())
        elif browser == 'ie':
            driver_instance = selenium_web_driver.Ie(IEDriverManager().install())
        elif browser == 'edge':
            driver_instance = selenium_web_driver.Edge(EdgeChromiumDriverManager().install())
        elif browser == 'safari':
            driver_instance = selenium_web_driver.Safari()

        elif browser == 'appium':
            desired_caps = {
                "deviceName": read_config_file("appium", 'deviceName'),
                "platformName": read_config_file("appium", 'platformName'),
                "app": read_config_file("appium", 'app'),
                "appPackage": read_config_file("appium", 'appPackage'),
                "appActivity": read_config_file("appium", 'appActivity'),
            }
            driver_instance = appium_web_driver.Remote(read_config_file("appium", 'server'), desired_caps)
        elif browser == 'browserstack':
            user_name = os.environ['BROWSERSTACK_USERNAME']
            access_key = os.environ['BROWSERSTACK_ACCESS_KEY']
            # Se intentaran leer las variables para configurar la ejecucion en BrowserStack usando un dispositivo mobile
            try:
                desired_cap = {
                    "browserName": os.environ["browserName"] if os.environ[
                                                                    "browserName"] != 'none' else read_config_file(
                        "browserstack", 'browserName'),
                    "device": os.environ["device"] if os.environ["device"] != 'none' else read_config_file(
                        "browserstack",
                        'device'),
                    "os_version": os.environ["os_version"] if os.environ["os_version"] != 'none' else read_config_file(
                        "browserstack", 'os_version')
                }
            # Si no es posible leer alguna de estas variables requeridas, se leeran las variables para una sesion desktop en BS
            except:
                desired_cap = {
                    "browser": os.environ["bs_browser"] if os.environ["bs_browser"] != 'none' else read_config_file(
                        "browserstack", 'browser'),
                    "browser_version": os.environ["bs_browser_version"] if os.environ[
                                                                               "bs_browser_version"] != 'none' else read_config_file(
                        "browserstack", 'browser_version'),
                    "os": os.environ["bs_os"] if os.environ["bs_os"] != 'none' else read_config_file("browserstack",
                                                                                                     'os'),
                    "os_version": os.environ["os_version"] if os.environ["os_version"] != 'none' else read_config_file(
                        "browserstack", 'os_version')
                }

            desired_cap["project"] = read_config_file("browserstack", 'project')
            desired_cap["build"] = read_config_file("browserstack", 'build')
            desired_cap["name"] = read_config_file("browserstack", 'name')

            driver_instance = selenium_web_driver.Remote(
                "http://" + user_name + ":" + access_key + "@hub-cloud.browserstack.com/wd/hub",
                desired_cap)
        else:
            raise Exception(f'"{browser}" is not a supported browser')

        if headless and maximized:
            driver_instance.set_window_size('1440', '700')
        elif maximized:
            driver_instance.maximize_window()

        # Wait implicitly for elements to be ready before attempting interactions
        driver_instance.implicitly_wait(config_implicit_timeout())
        set_driver_type()

    return driver_instance


def set_driver_type():
    """
        Esta funcion genera una variable de sistema llamada driver_type.
        Si alguno de los parametros que generan una ejecucion en un dispositivo mobile no está vacio se setea el
        driver_type = mobile, caso contrario será desktop
    """
    config_device_name = read_config_file_with_validation("driver", 'device_name')
    config_device = read_config_file_with_validation("browserstack", 'device')
    os_device_name = os.environ["device_name"]
    os_device = os.environ["device"]

    os.environ["driver_type"] = 'mobile' if (config_device_name is not None or
                                             config_device is not None or
                                             os_device_name != 'none' or
                                             os_device != 'none') else 'desktop'
