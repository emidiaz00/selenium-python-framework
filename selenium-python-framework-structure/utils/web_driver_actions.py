import logging
import os
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from utils import driver_config
from utils.driver_config import get_driver_instance, config_implicit_timeout, config_browser


def locator_by(selector):
    strategy = selector.get('BY')
    locator = selector.get('LOCATOR')
    return strategy, locator


class WebDriverActions:
    ENV = os.getenv('env')

    def __init__(self, driver):
        self.driver = driver
        explicit_timeout = driver_config.config_explicit_timeout()
        self.wait = WebDriverWait(driver=self.driver, timeout=explicit_timeout)

    def is_desktop_driver(self):
        return os.environ["driver_type"] == 'desktop'

    def navigate_to(self, url: str):
        """Navigates to an URL"""
        logging.info(f"NAVIGATE TO {url}")
        get_driver_instance().get(url)

    def get_url(self):
        return get_driver_instance().current_url

    def switch_to_windows(self, index):
        driver = get_driver_instance()
        driver.switch_to.window(driver.window_handles[index])

    def refresh(self):
        get_driver_instance().refresh()

    def verify_text_on_title_page(self, text):
        return self.wait_text_on_title_contains_and_verify(text)

    def verify_url_page_contains(self, text):
        return self.wait_url_contains_and_verify(text)

    def get_element(self, locator: str):
        """Gets an element based on a selector and a strategy"""
        strategy, selector = locator
        logging.info(f"FIND ELEMENT {selector} BY {strategy}")
        self.__treatment_for_safari(locator)
        element = self.driver.find_element(strategy, selector)
        return element

    def get_elements(self, locator: str):
        """Gets an array of elements based on a selector and a strategy"""
        strategy, selector = locator
        logging.info(f"FIND ELEMENT {selector} BY {strategy}")
        self.__treatment_for_safari(locator)
        elements = self.driver.find_elements(strategy, selector)
        return elements

    def __treatment_for_safari(self, locator):
        if config_browser() == 'safari':
            get_driver_instance().implicitly_wait(1)
            try:
                strategy, selector = locator
                local_wait = WebDriverWait(driver=self.driver, timeout=5)
                local_wait.until(expected_conditions.presence_of_element_located((strategy, selector)))
                local_wait = WebDriverWait(driver=self.driver, timeout=5)
                local_wait.until(expected_conditions.element_to_be_clickable((strategy, selector)))
            except:
                pass
            get_driver_instance().implicitly_wait(config_implicit_timeout())

    def is_text_equal(self, element_text, expected_text):
        if config_browser() == 'safari':
            return element_text == str(expected_text).replace('\n', '')
        else:
            return element_text == expected_text

    def wait_for_element(self, locator: str):
        """Waits for an element based on a selector and a strategy"""
        strategy, selector = locator
        logging.info(f"WAIT FOR ELEMENT {selector}")
        return self.wait.until(expected_conditions.presence_of_element_located((strategy, selector)))

    def wait_element_contain_text(self, locator: str, text):
        """Waits for element contains required text based on a selector, a strategy and text provided"""
        strategy, selector = locator
        logging.info(f"WAIT FOR TEXT {text} ON ELEMENT {selector}")
        return self.wait.until(expected_conditions.text_to_be_present_in_element((strategy, selector), text))

    def wait_element_with_not_empty_text(self, locator: str):
        """Waits for text on an element based on a selector and a strategy"""
        strategy, selector = locator
        logging.info(f"WAIT FOR SOME TEXT ON ELEMENT {selector}")
        return self.wait.until(lambda driver: self.get_element(locator).text.strip() != '')

    def wait_for_invisibility_of_element(self, locator: str):
        """Waits for an element based on a selector and a strategy"""
        strategy, selector = locator
        logging.info(f"WAIT FOR INVISIBILITY OF ELEMENT {selector}")
        get_driver_instance().implicitly_wait(2)
        self.wait.until(expected_conditions.invisibility_of_element_located((strategy, selector)))
        get_driver_instance().implicitly_wait(config_implicit_timeout())
        time.sleep(1)

    def wait_for_clickablility_of_element(self, locator: str):
        """Waits for an element based on a selector and a strategy"""
        strategy, selector = locator
        logging.info(f"WAIT FOR CLICKABILITY OF ELEMENT {selector}")
        self.wait.until(expected_conditions.element_to_be_clickable((strategy, selector)))

    def wait_text_on_title_contains_and_verify(self, title):
        """Waits for text in Title Page, if the text is displayed on page returns True,
           if it is not displayed return False"""
        logging.info(f"WAIT FOR TEXT {title} ON PAGE")
        try:
            self.wait.until(expected_conditions.title_contains(title))
            return True
        except:
            return False

    def wait_url_contains_and_verify(self, text):
        """Waits for text in url, if the text is displayed on url returns True,
           if it is not displayed return False"""
        logging.info(f"WAIT FOR TEXT {text} ON URL")
        try:
            self.wait.until(expected_conditions.url_contains(text))
            return True
        except:
            return False

    def element_exist(self, locator: str):
        """Checks the existence of an element based on a selector and a strategy"""
        logging.info("CHECK ELEMENT EXISTENCE")
        elements = self.get_elements(locator)
        if len(elements) == 0:
            return False
        else:
            return True

    def is_element_displayed(self, locator: str, with_implicit_timeout=True):
        """Checks the visibility of an element based on a selector and a strategy"""
        strategy, selector = locator
        logging.info(f"CHECK VISIBILITY OF ELEMENT {selector}")
        response = False
        if not with_implicit_timeout:
            get_driver_instance().implicitly_wait(1)
        elements = self.get_elements(locator)
        if len(elements) > 0 and elements[0].is_displayed():
            response = True
        if not with_implicit_timeout:
            get_driver_instance().implicitly_wait(config_implicit_timeout())
        return response

    def is_element_not_displayed(self, locator: str):
        """Checks the invisibility of an element based on a selector and a strategy"""
        return False if self.is_element_displayed(locator, False) else True

    def is_element_enabled(self, locator: str):
        """Checks if element is enabled based on a selector and a strategy"""
        strategy, selector = locator
        logging.info(f"CHECK CLICKABILITY OF ELEMENT {selector}")
        elements = self.get_elements(locator)
        if len(elements) == 0:
            raise Exception("Element was not found")
        elif elements[0].is_enabled():
            return True
        else:
            return False

    def is_element_checked(self, locator: str):
        """Checks if element is checked based on a selector and a strategy"""
        logging.info("CHECK ELEMENT IS CHECKED")
        elements = self.get_elements(locator)
        if len(elements) == 0:
            return False
        elif elements[0].get_attribute("checked"):
            return True
        else:
            return False

    def get_element_attribute(self, locator: str, attribute):
        """Gets an attribute element based on a selector and attribute name"""
        strategy, selector = locator
        logging.info(f"FIND ATTRIBUTE {attribute} ON ELEMENT {selector}")
        elements = self.get_elements(locator)
        if len(elements) == 0:
            return ""
        else:
            return elements[0].get_attribute(attribute)

    def click_element(self, locator: str):
        """Click an element based on a selector and a strategy"""
        strategy, selector = locator
        logging.info(f"CLICK ON ELEMENT {selector}")
        elements = self.get_elements(locator)
        if len(elements) != 0:
            elements[0].click()
        else:
            raise Exception(f'No se encontró el elemento {selector}')

    def get_text_element(self, locator: str):
        """Get text on element based on a selector and a strategy"""
        strategy, selector = locator
        logging.info(f"GET TEXT ON ELEMENT {selector}")
        elements = self.get_elements(locator)
        if len(elements) != 0:
            return elements[0].text
        else:
            raise Exception(f'No se encontró el elemento {selector}')

    def send_keys_to_element(self, locator: str, text):
        """Send keys to element based on a selector and a strategy"""
        strategy, selector = locator
        logging.info(f"SEND KEYS {text} TO ELEMENT {selector}")
        elements = self.get_elements(locator)
        if len(elements) != 0:
            elements[0].send_keys(text)
        else:
            raise Exception(f'No se encontró el elemento {selector}')

    def select_option(self, select_element_locator, selected_option):
        time.sleep(2)
        select = self.wait_for_element(select_element_locator)
        options = select.find_elements_by_tag_name('option')
        option_found = False
        for option in options:
            if option.text.strip().upper() == selected_option.strip().upper():
                option.click()
                option_found = True
                break
        if not option_found:
            raise Exception(f'La opción {selected_option} no se encontró en la lista')

    def check_options_from_select(self, select_element_locator, options_list):
        select = self.get_element(select_element_locator)
        options = select.find_elements_by_tag_name('option')
        valid_select_list = True
        for option in options:
            if option.text.strip() not in options_list:
                valid_select_list = False
                break
        return valid_select_list

    def upload_file(self, file_element_locator, file_path):
        file_input = self.get_element(file_element_locator)
        file_input.send_keys(file_path)

    def scroll_to_the_bottom_of_the_page(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    def scroll_to_element(self, locator):
        """Scroll to element based on a selector and a strategy"""
        strategy, selector = locator
        logging.info(f"CLEAN TEXT IN ELEMENT {selector}")
        elements = self.get_elements(locator)
        actions = ActionChains(self.driver)
        if len(elements) != 0:
            actions.move_to_element(elements[0]).perform()
        else:
            raise Exception(f'No se encontró el elemento {selector}')

    def clean_input(self, locator):
        """Clean keys to element based on a selector and a strategy"""
        strategy, selector = locator
        logging.info(f"CLEAN TEXT IN ELEMENT {selector}")
        elements = self.get_elements(locator)
        if len(elements) != 0:
            elements[0].clear()
            elements[0].send_keys(Keys.HOME)
        else:
            raise Exception(f'No se encontró el elemento {selector}')