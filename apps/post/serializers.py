from rest_framework import serializers
from .models import Post

HUMAN_DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S%Z'


class PostSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format=HUMAN_DATETIME_FORMAT)
    last_update = serializers.DateTimeField(format=HUMAN_DATETIME_FORMAT)

    class Meta:
        model = Post
        fields = '__all__'
