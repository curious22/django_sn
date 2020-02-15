from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.post import serializers
from .models import Post


class PostResource(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = Post.objects.all()
        serializer = serializers.DetailPostSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = serializers.CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)
        return Response({'id': post.id}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = serializers.DetailPostSerializer(user)
        return Response(serializer.data)
