import time

import allure
import pytest
from assertpy import assert_that

from pages import login_page
from pages.login_page import LoginPageAutomationPractice
from utils.data_loader import DataLoader


class TestLogin():
    def setup_class(self):
        self._data = DataLoader.get_data_from_ini_file("user_data.ini")

    def test_verify_home_page_us_open(self, open_login_page_AUTO):
        login_page = open_login_page_AUTO
        assert login_page.is_displayed()
        home_page = login_page.login(self._data.usuario, self._data.contrasena)
        assert home_page.is_displayed()
        time.sleep(5)

    def test_verify_login_title(self, open_login_page_AUTO):
        login_page = open_login_page_AUTO
        assert login_page.is_displayed()
        home_page = login_page.login(self._data.usuario, self._data.contrasena)
        assert ("My account - My Store" in login_page.get_page_title())

    def test_msg_my_account(self, open_login_page_AUTO):
        login_page = open_login_page_AUTO
        home_page = login_page.login(self._data.usuario, self._data.contrasena)
        msg = "Welcome to your account. Here you can manage all of your personal information and orders."
        assert login_page.result_account_was_created() == msg
