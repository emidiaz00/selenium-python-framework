import json
import logging

import requests
import pytest
from assertpy import assert_that
from apis.api_new_coin import ApiBraveNewCoinQA


class TestApiBraveNewCoin:
    def setup_class(self):
        logging.info("Llamando al constructor de la api")
        self.api_new_coin = ApiBraveNewCoinQA()

    def test_verificar_status_code(self):
        response = self.api_new_coin.get_validar_status_code()
        assert_that(response.status_code).is_equal_to(200)
