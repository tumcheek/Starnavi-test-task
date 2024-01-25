import random
import logging
from urllib.parse import urljoin
import requests
from faker import Faker
from config import BASE_URL


USERS_URL = 'users/'
POSTS_URL = 'posts/'
TOKEN_URL = 'token/'
LIKE_URL = 'like/'
FAKE = Faker()


def create_user() -> dict:
    full_url = urljoin(BASE_URL, USERS_URL)
    data = {
        'username': FAKE.user_name(),
        'password': FAKE.password()
    }
    response = requests.post(full_url, data=data)
    if response.status_code == 400:
        raise ValueError(response.text)
    return data


def get_user_access_token(user_data: dict) -> str:
    full_url = urljoin(BASE_URL, TOKEN_URL)
    response = requests.post(full_url, data=user_data)
    if response.status_code == 400 or response.status_code == 401 or response.status_code == 415:
        raise ValueError(response.text)
    return response.json()['access']


def create_post(jwt_token: str) -> dict:
    full_url = urljoin(BASE_URL, POSTS_URL)

    headers = {
        'Authorization': f'Bearer {jwt_token}',
    }

    data = {
        'title': FAKE.word(),
        'body': FAKE.words(),
    }

    response = requests.post(full_url, data=data, headers=headers)
    if response.status_code == 401:
        raise ValueError(response.json()['detail'])

    return response.json()


def create_like(jwt_token: str, post_id: int) -> None:
    full_url = urljoin(BASE_URL, f'{POSTS_URL}/{post_id}/{LIKE_URL}')
    headers = {
        'Authorization': f'Bearer {jwt_token}',
    }

    response = requests.post(full_url, headers=headers)

    if response.status_code == 422 or response.status_code == 401:
        raise ValueError(response.json()['error'])


def generate_user_access_tokens(number_of_users: int) -> list:
    users_tokens = []
    for _ in range(number_of_users):
        try:
            user = create_user()
            users_tokens.append(get_user_access_token(user))
        except ValueError as e:
            logging.error(e)
    return users_tokens


def create_dummy_posts(users_tokens: list, max_posts_per_user: int) -> list:
    posts = []
    for user_token in users_tokens:
        for _ in range(random.randint(1, max_posts_per_user)):
            posts.append(create_post(user_token)['id'])
    return posts


def create_random_likes_for_posts(users_tokens: list, posts: list, max_likes_per_user: int) -> None:
    posts_number = len(posts) - 1
    for user_token in users_tokens:
        for _ in range(max_likes_per_user):
            try:
                create_like(user_token, posts[random.randint(1, posts_number)])
            except ValueError as e:
                logging.error(e)
