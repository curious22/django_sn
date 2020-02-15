from rest_framework import serializers

from .models import Post

HUMAN_DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S %Z'


class CreatePostSerializer(serializers.ModelSerializer):
    """
    Serializer for creat a new Post
    Required fields: author, title, text
    """
    created = serializers.DateTimeField(format=HUMAN_DATETIME_FORMAT, read_only=True)
    last_update = serializers.DateTimeField(format=HUMAN_DATETIME_FORMAT, read_only=True)

    class Meta:
        model = Post
        exclude = ('author',)


class DetailPostSerializer(CreatePostSerializer):
    """Serializer for getting detail info about Post"""
    class Meta:
        model = Post
        fields = '__all__'
