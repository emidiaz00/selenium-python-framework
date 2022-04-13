"""
Precondiciones que pueden ser utilizadas en todos los casos de prueba
"""
import pytest

from pages.login_page import LoginPageAutomationPractice


@pytest.fixture()
def open_login_page_AUTO(driver):
    login_page = LoginPageAutomationPractice()
    login_page.go()
    assert login_page.is_displayed()
    return login_page
