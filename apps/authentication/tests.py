from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


def create_user():
    """Shortcut for quick user creation"""
    return get_user_model().objects.create_user(
        email='test@user.com',
        password='some password',
        first_name='Jhon',
        last_name='Doe'
    )


class TestRegistrationEndpoint(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.endpoint = '/api/v1/auth/registration/'

    def setUp(self):
        super().setUp()
        self.user_data = {
            'email': 'test@user.com',
            'password': 'some password',
            'first_name': 'Jhon',
            'last_name': 'Doe',
        }

    def test_create_user(self):
        resp = self.client.post(self.endpoint, self.user_data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertNotEqual(
            get_user_model().objects.get(pk=1).password,
            self.user_data['password'])

    def test_create_duplicate_user(self):
        resp = self.client.post(self.endpoint, self.user_data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = self.client.post(self.endpoint, self.user_data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user(self):
        resp = self.client.get(self.endpoint)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_user_without_email(self):
        self.user_data.pop('email')

        resp = self.client.post(self.endpoint, self.user_data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.json(), {'email': ['This field is required.']})

    def test_create_user_without_password(self):
        self.user_data.pop('password')

        resp = self.client.post(self.endpoint, self.user_data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.json(), {'password': ['This field is required.']})


class TestAuthLogin(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.endpoint = '/api/v1/auth/login/'

    def setUp(self):
        super().setUp()
        self.user = create_user()
        self.user_cred = {
            'email': 'test@user.com',
            'password': 'some password',
        }

    def test_login_user_exists(self):
        resp = self.client.post(self.endpoint, data=self.user_cred)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', resp.json())
        self.assertIn('refresh', resp.json())

    def test_login_user_not_existed(self):
        resp = self.client.post(
            self.endpoint,
            data={'email': 'base@user.com', 'password': 'pass123'})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', resp.json())
        self.assertNotIn('refresh', resp.json())


class TestAuthTokenRefresh(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.endpoint = '/api/v1/auth/token/refresh/'

    def setUp(self):
        super().setUp()
        self.user = create_user()
        self.user_cred = {
            'email': 'test@user.com',
            'password': 'some password',
        }

    def test_token_refresh_success(self):
        resp = self.client.post(
            '/api/v1/auth/login/',
            data=self.user_cred)
        refresh_token = resp.json()['refresh']
        access_token = resp.json()['access']

        resp = self.client.post(self.endpoint, data={'refresh': refresh_token})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', resp.json())
        self.assertNotEqual(access_token, resp.json()['access'])
