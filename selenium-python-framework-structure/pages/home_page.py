import logging

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.web_driver_actions import locator_by

class HomePageAutomation(BasePage):

    __DIV_CONTAINER = locator_by({
        'BY': By.XPATH,
        'LOCATOR': "//header/div[1]/div[1]"
    })

    def __init__(self):
        super().__init__()

    def is_displayed(self):
        try:
            self.wait_for_element(self.__DIV_CONTAINER)
            return True
        except:
            logging.error("No se visualiza la pantalla del Home Page.")
            return False