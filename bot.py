import json
import os
import sys
from collections import namedtuple

import requests
from faker import Faker
from requests import exceptions

CONFIG_FILE = 'bot_config.json'
BASE_URL = 'http://localhost:8000/api/v1'
SESSION = requests.Session()
FAKE = Faker()
User = namedtuple('User', 'email access')

API_MAPPER = {
    'sigup': f'{BASE_URL}/auth/registration/',
    'login': f'{BASE_URL}/auth/login/',
    'create_post': f'{BASE_URL}/posts/',
    'like': f'{BASE_URL}/likes/'
}


def get_config(file_name):
    with open(file_name) as _file:
        return json.load(_file)


def validate_config(config):
    expected_keys = {
        'number_of_users',
        'max_posts_per_user',
        'max_likes_per_user'
    }
    keys = set(config.keys())
    if not expected_keys.issubset(keys):
        print(f'Config file does not have all params: {expected_keys - keys}')
        sys.exit(1)

    for key in keys:
        if config[key] <= 0:
            print(f'Parameter "{key}" must be greater than zero')
            sys.exit(1)


def check_api(url):
    """Checks API availability"""
    try:
        resp = SESSION.get(url)
        if resp.status_code != 200:
            return False
    except exceptions.RequestException as err:
        print(f'API host has not available: {err}')
        return False

    return True


def get_fake_user():
    """Generate a fake user for signup"""
    data = {
        'email': FAKE.email(),
        'password': 'pass',
        'first_name': FAKE.first_name(),
        'last_name': FAKE.last_name()
    }
    return data


def user_login(cred):
    """Get access token to registered user"""
    resp = SESSION.post(API_MAPPER['login'], cred)
    if resp.status_code == 200:
        print(f'User {cred["email"]} has logined')
        return resp.json()['access']
    return False


def user_registration(user):
    """Register user and login (get access token)"""""
    resp = SESSION.post(API_MAPPER['sigup'], user)
    if resp.status_code == 201:
        print(f'User {user["email"]} has registered')
        access = user_login(user)
        return User(user['email'], access)

    return False


if __name__ == '__main__':
    if not os.path.exists(CONFIG_FILE):
        print('Config file does not exist. Create it before using a bot')
        sys.exit(1)

    config = get_config(CONFIG_FILE)
    validate_config(config)
    check_api(BASE_URL)
    users = []

    # create users
    for _ in range(config['number_of_users']):
        email = user_registration(get_fake_user())
        if email:
            users.append(email)

    print(users)
