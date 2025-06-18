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


def test_get_read_papers(username):
    url = f"{BASE_URL}/users/read_papers"
    params = {"username": username}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(f"GET /users/read_papers for {username} successful:", response.json())
    else:
        print(
            f"GET /users/read_papers for {username} failed with status code:",
            response.status_code,
        )


def test_set_read_papers(username, read_paper_ids):
    url = f"{BASE_URL}/users/read_papers"
    payload = {"username": username, "arxiv_ids": read_paper_ids}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"POST /users/read_papers for {username} successful:", response.json())
    else:
        print(
            f"POST /users/read_papers for {username} failed with status code:",
            response.status_code,
        )


def test_get_favorite_papers(username):
    url = f"{BASE_URL}/users/favorite_papers"
    params = {"username": username}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(f"GET /users/favorite_papers for {username} successful:", response.json())
    else:
        print(
            f"GET /users/favorite_papers for {username} failed with status code:",
            response.status_code,
        )


def test_set_favorite_papers(username, favorite_paper_ids):
    url = f"{BASE_URL}/users/favorite_papers"
    payload = {"username": username, "arxiv_ids": favorite_paper_ids}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(
            f"POST /users/favorite_papers for {username} successful:", response.json()
        )
    else:
        print(
            f"POST /users/favorite_papers for {username} failed with status code:",
            response.status_code,
        )


def test_analyze_paper(arxiv_id: str, section: str):
    url = f"{BASE_URL}/analysis"
    payload = {"arxiv_id": arxiv_id, "section": section}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"POST /analysis for {arxiv_id} successful:", response.json())
    else:
        print(
            f"POST /analysis for {arxiv_id} failed with status code:",
            response.status_code,
        )


if __name__ == "__main__":
    # test_get_users()

    # start_time = int(datetime(2020, 1, 1).timestamp())
    # end_time = int(datetime(2025, 3, 1).timestamp())
    # test_post_query(
    #    ["large language model", "reasoning", "reinforcement learning"],
    #    start_time,
    #    end_time,
    # )

    # test_get_keywords("liziheng")
    # test_post_keywords("arkcia", ["meta-learning", "Function Vector"])

    # test_set_read_papers("liziheng", ["2311.00001", "2311.00002"])
    # test_get_read_papers("liziheng")
    # test_set_favorite_papers("liziheng", ["2311.00001", "2311.00002"])
    # test_get_favorite_papers("liziheng")

    test_analyze_paper("2506.02208", "method")
