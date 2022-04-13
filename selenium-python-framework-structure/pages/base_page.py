from utils.driver_config import get_driver_instance
from utils.web_driver_actions import WebDriverActions


class BasePage(WebDriverActions):

    def __init__(self):
        super().__init__(get_driver_instance())
