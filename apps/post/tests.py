from rest_framework import status
from rest_framework.test import APIClient

from apps.authentication.tests import BaseTestClass
from .models import Post
from .serializers import PostSerializer


class TestPostResource(BaseTestClass):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.endpoint = '/api/v1/posts/'

    def setUp(self):
        super().setUp()
        self.post = Post.objects.create(
            author=self.base_user,
            title='Test title',
            text='Lorem ipsum'
        )

    def test_get_posts_unauth(self):
        anonimus = APIClient()
        resp = anonimus.get(self.endpoint)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_posts_success(self):
        resp = self.client.get(self.endpoint)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        expected = PostSerializer(
            Post.objects.all(),
            many=True).data
        self.assertEqual(resp.json(), expected)
