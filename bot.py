import json
import os
import sys
from collections import namedtuple
from random import choice

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


def api_is_available(url):
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


def get_fake_post():
    text = FAKE.text()
    title = text.split('.')[0]
    data = {
        'title': title[:45],
        'text': text
    }
    return data


def create_post(user):
    """
    Create a post by user
    Return id of created post
    """
    post = get_fake_post()
    headers = {'authorization': f'Bearer {user.access}'}

    resp = SESSION.post(API_MAPPER['create_post'], post, headers=headers)
    if resp.status_code == 201:
        title = post['title']
        print(f'Post "{title}" has created by {user.email}')
        return resp.json()['id']


def like_post(user, post_id):
    """
    Like or unlike a post
    (if post has already liked by the same user)
    """
    headers = {'authorization': f'Bearer {user.access}'}
    resp = SESSION.post(
        API_MAPPER['like'],
        {'post': post_id},
        headers=headers)
    if resp.status_code in (200, 201):
        print(resp.json()['detail'])


if __name__ == '__main__':
    if not os.path.exists(CONFIG_FILE):
        print('Config file does not exist. Create it before using a bot')
        sys.exit(1)

    config = get_config(CONFIG_FILE)
    validate_config(config)
    if not api_is_available(BASE_URL):
        sys.exit(1)

    users = []  # users credential
    posts = []  # ids of created posts

    print('Create users')
    for _ in range(config['number_of_users']):
        email = user_registration(get_fake_user())
        if email:
            users.append(email)
    print()

    print('Create posts')
    for user in users:
        for post in range(config['max_posts_per_user']):
            posts.append(create_post(user))
        print()

    print('Like posts')
    for user in users:
        for _ in range(config['max_likes_per_user']):
            like_post(user, choice(posts))
        print()
