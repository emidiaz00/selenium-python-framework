from selenium.webdriver.remote.webelement import WebElement

from utils.web_driver_actions import WebDriverActions


class BaseObject(WebDriverActions):

    def __init__(self, container: WebElement):
        super().__init__(container)
