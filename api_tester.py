import json
from datetime import datetime

import requests

BASE_URL = "http://172.29.2.84:5000"  # Replace with the actual base URL of the API


def test_get_users():
    url = f"{BASE_URL}/users"
    response = requests.get(url)
    if response.status_code == 200:
        print("GET /users successful:", response.json())
    else:
        print("GET /users failed with status code:", response.status_code)


def test_post_query(query: list[str], start_time: int, end_time: int):
    url = f"{BASE_URL}/query"
    payload = {
        "query": query,
        "start_time": start_time,
        "end_time": end_time,
        "start_index": 0,
        "end_index": 10,
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("POST /query successful:", response.json())
    else:
        print("POST /query failed with status code:", response.status_code)


def test_get_keywords(username):
    url = f"{BASE_URL}/keywords"
    params = {"username": username}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(f"GET /keywords for {username} successful:", response.json())
    else:
        print(
            f"GET /keywords for {username} failed with status code:",
            response.status_code,
        )


def test_post_keywords(username, keywords):
    url = f"{BASE_URL}/keywords"
    payload = {"username": username, "keywords": keywords}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"POST /keywords for {username} successful:", response.json())
    else:
        print(
            f"POST /keywords for {username} failed with status code:",
            response.status_code,
        )


if __name__ == "__main__":
    test_get_users()

    start_time = int(datetime(2024, 1, 1).timestamp())
    end_time = int(datetime(2024, 3, 1).timestamp())
    test_post_query("meta-learning", start_time, end_time)

    test_get_keywords("liziheng")
    test_post_keywords("arkcia", ["meta-learning", "Function Vector"])
