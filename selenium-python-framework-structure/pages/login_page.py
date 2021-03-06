import logging

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.home_page import HomePageAutomation
from utils.config_loader import read_config_from_current_env
from utils.web_driver_actions import locator_by


class LoginPageAutomationPractice(BasePage):
    __HEADER_CONTAINER = locator_by({
        'BY': By.ID,
        'LOCATOR': "header"
    })

    __SIGN_IN_BUTTON = locator_by({
        'BY': By.XPATH,
        'LOCATOR': "//a[contains(text(),'Sign in')]"
    })

    __INPUT_EMAIL = locator_by({
        'BY': By.NAME,
        'LOCATOR': "email"
    })

    __INPUT_PASSWORD = locator_by({
        'BY': By.XPATH,
        'LOCATOR': "//input[@id='passwd']"
    })

    __BTN_LOGIN = locator_by({
        'BY': By.ID,
        'LOCATOR': "SubmitLogin"
    })

    __MY_ACCOUNT = locator_by({
        'BY': By.XPATH,
        'LOCATOR': "//h1[contains(text(),'My account')]"
    })

    __MY_ACCOUNT_MSG = locator_by({
        'BY': By.XPATH,
        'LOCATOR': "//p[contains(text(),'Welcome to your account. Here you can manage all o')]"
    })

    def __init__(self):
        super().__init__()

    def go(self):
        servicios_url = read_config_from_current_env('base_url')
        self.navigate_to(url=servicios_url)

    def is_displayed(self):
        try:
            self.wait_for_element(self.__HEADER_CONTAINER)
            return True
        except:
            logging.error("No se visualiza la pantalla del login.")
            return False

    def click_login(self):
        self.wait_for_clickablility_of_element(self.__SIGN_IN_BUTTON)
        self.click_element(self.__SIGN_IN_BUTTON)

    def fill_input_email(self, email):
        self.send_keys_to_element(self.__INPUT_EMAIL, email)

    def fill_input_password(self, password):
        self.send_keys_to_element(self.__INPUT_PASSWORD, password)

    def click_on_login_btn(self):
        self.click_element(self.__BTN_LOGIN)

    def login(self, username, password):
        self.click_login()
        self.fill_input_email(username)
        self.fill_input_password(password)
        self.click_on_login_btn()
        return HomePageAutomation()

    def get_page_title(self):
        return self.driver.title

    def result_account_was_created(self):
        return self.get_text_element(self.__MY_ACCOUNT_MSG)












