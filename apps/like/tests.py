from rest_framework import status
from rest_framework.test import APIClient

from apps.authentication.tests import BaseTestClass
from apps.post.models import Post
from .models import Like


class TestPostResource(BaseTestClass):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.endpoint = '/api/v1/likes/'

    def setUp(self):
        super().setUp()
        self.post = Post.objects.create(
            author=self.base_user,
            title='Test title',
            text='Lorem ipsum'
        )

    def test_create_like_unauth(self):
        anonimus = APIClient()
        resp = anonimus.post(self.endpoint)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_like_success(self):
        resp = self.client.post(self.endpoint, {'post': self.post.pk})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(
            resp.json(),
            {'detail': 'Post "Test title" has liked by test@user.com'}
        )

    def test_unlike_success(self):
        resp = self.client.post(self.endpoint, {'post': self.post.pk})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

        resp = self.client.post(self.endpoint, {'post': self.post.pk})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(Like.objects.count(), 0)
        self.assertEqual(
            resp.json(),
            {'detail': 'Post 1 has unliked by test@user.com'}
        )
