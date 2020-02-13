from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


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

    def is_user_can_login(self, access_data):
        endpoint = '/api/v1/auth/login/'
        req = self.client.post(endpoint, access_data)
        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertIn('access', req.json())
        self.assertIn('refresh', req.json())

    def test_create_user(self):
        req = self.client.post(self.endpoint, self.user_data)
        self.assertEqual(req.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertNotEqual(
            get_user_model().objects.get(pk=1).password,
            self.user_data['password'])

        access_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        self.is_user_can_login(access_data)

    def test_create_duplicate_user(self):
        req = self.client.post(self.endpoint, self.user_data)
        self.assertEqual(req.status_code, status.HTTP_201_CREATED)

        req = self.client.post(self.endpoint, self.user_data)
        self.assertEqual(req.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user(self):
        req = self.client.get(self.endpoint)
        self.assertEqual(req.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_user_without_email(self):
        self.user_data.pop('email')

        req = self.client.post(self.endpoint, self.user_data)
        self.assertEqual(req.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(req.json(), {'email': ['This field is required.']})

    def test_create_user_without_password(self):
        self.user_data.pop('password')

        req = self.client.post(self.endpoint, self.user_data)
        self.assertEqual(req.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(req.json(), {'password': ['This field is required.']})
