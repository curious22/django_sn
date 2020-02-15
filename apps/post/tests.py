from rest_framework import status
from rest_framework.test import APIClient

from apps.authentication.tests import BaseTestClass, create_user
from .models import Post
from .serializers import DetailPostSerializer


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

    def test_create_post_duplicate_title(self):
        self.new_post['title'] = 'Test title 2'
        resp = self.client.post(self.endpoint, self.new_post)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            resp.json(),
            {'title': ['post with this title already exists.']}
        )

    def test_create_post_without_text(self):
        self.new_post['text'] = ''
        resp = self.client.post(self.endpoint, self.new_post)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            resp.json(),
            {'text': ['This field may not be blank.']}
        )

    def test_create_post_without_title(self):
        self.new_post['title'] = ''
        resp = self.client.post(self.endpoint, self.new_post)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            resp.json(),
            {'title': ['This field may not be blank.']}
        )

    def test_get_post_unauth(self):
        anonimus = APIClient()
        resp = anonimus.get(f'{self.endpoint}{self.post.id}/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_post_not_exists(self):
        resp = self.client.get(f'{self.endpoint}999/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_post_success(self):
        resp = self.client.get(f'{self.endpoint}{self.post.id}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        expected = DetailPostSerializer(
            Post.objects.get(pk=self.post.pk)).data
        self.assertEqual(resp.json(), expected)

    def test_update_post(self):
        resp = self.client.post(f'{self.endpoint}{self.post.id}/')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
