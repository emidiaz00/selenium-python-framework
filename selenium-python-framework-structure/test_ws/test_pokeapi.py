import json

import requests
from assertpy.assertpy import assert_that

BASE_URL = "https://pokeapi.co/api/v2/pokemon/?limit=20"

def test_get_pokemon():
    url = BASE_URL
    response = requests.get(url=url)
    assert response.status_code == 200
