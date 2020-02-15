from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import Like
from .serializers import LikeSerializer


class LikeResource(ViewSet):
    """Resource for create and delete likes"""
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        """
        POST /likes/ {'post': <pk>}
        If post has already liked - remove like from this post by selected user

        :param request:
        :return: 201 for liked and 200 for unliked post
        """
        data = dict()
        data['post'] = request.data['post']
        data['user'] = request.user.pk

        serializer = LikeSerializer(data=data)
        if serializer.is_valid():
            like = serializer.save(user=request.user)
            return Response(
                {'datail': f'Post "{like.post.title}" has liked by {like.user}'},
                status=status.HTTP_201_CREATED
            )

        # post has already liked
        existed_like = Like.objects.filter(post=data['post'], user=request.user)
        existed_like.delete()
        return Response(
            {'datail': f'Post {data["post"]} has unliked by {request.user}'},
            status=status.HTTP_200_OK
        )
