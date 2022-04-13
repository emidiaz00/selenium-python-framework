import time

import allure
import pytest

from utils.data_loader import DataLoader


class TestLogin:

    def setup_class(self):
        self._data = DataLoader.get_data_from_ini_file("user_data.ini")

    def test_verify_home_page_us_open(self, open_login_page_AUTO):
        login_page = open_login_page_AUTO
        assert login_page.is_displayed()
        home_page = login_page.login(self._data.usuario, self._data.contrasena)
        assert home_page.is_displayed()
        time.sleep(5)
