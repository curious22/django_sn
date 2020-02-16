import json
import os
import sys

import requests
from faker import Faker
from requests import exceptions

CONFIG_FILE = 'bot_config.json'
BASE_URL = 'http://localhost:8000/api/v1'
SESSION = requests.Session()
FAKE = Faker()


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


if __name__ == '__main__':
    if not os.path.exists(CONFIG_FILE):
        print('Config file does not exist. Create it before using a bot')
        sys.exit(1)

    config = get_config(CONFIG_FILE)
    validate_config(config)
    check_api(BASE_URL)
