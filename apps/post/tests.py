from rest_framework import status
from rest_framework.test import APIClient

from apps.authentication.tests import BaseTestClass, create_user
from .models import Post
from .serializers import CreatePostSerializer, DetailPostSerializer


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
        Post.objects.create(
            author=create_user('new@email.com'),
            title='Test title 2',
            text='Lorem ipsum'
        )
        self.new_post = {
            'title': 'Test post 3',
            'text': 'New text'
        }

    def test_get_all_posts_unauth(self):
        anonimus = APIClient()
        resp = anonimus.get(self.endpoint)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_posts_success(self):
        resp = self.client.get(self.endpoint)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        expected = DetailPostSerializer(
            Post.objects.all(),
            many=True).data
        self.assertEqual(resp.json(), expected)

    def test_create_post_unauth(self):
        anonimus = APIClient()
        resp = anonimus.post(self.endpoint)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_success(self):
        resp = self.client.post(self.endpoint, self.new_post)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 3)
        self.assertEqual(resp.json(), {'id': Post.objects.last().id})
