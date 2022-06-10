import json
import requests
from assertpy.assertpy import assert_that


BASE_URL = "https://jsonplaceholder.typicode.com/"

def test_post_posts():
    path = "posts"
    url = BASE_URL + path
    payload = json.dumps({
       "title": "food",
        "body": "bar",
        "userId": 2
    })
    headers = {
        'Content-type': 'application/json; charset=UTF-8'
    }
    response = requests.post(url=url, data=payload, headers=headers)
    assert_that(response.status_code).is_equal_to(201)
