from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.post import serializers
from .models import Post


class PostResource(viewsets.ViewSet):
    """
    Resource for working with posts
    Authentication is required
    """
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        """
        GET /posts/
        :param request:
        :return: List of all posts
        """
        queryset = Post.objects.all()
        serializer = serializers.DetailPostSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        POST /posts/
        Create a new post
        :param request:
        :return: id of created post
        """
        serializer = serializers.CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)
        return Response({'id': post.id}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """
        GET /posts/<pk>/
        Get info about selected post
        :param request:
        :param pk: post id
        :return: Detail post info
        """
        queryset = Post.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = serializers.DetailPostSerializer(user)
        return Response(serializer.data)
