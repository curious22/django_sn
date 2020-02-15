from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for create Like from post and user"""

    class Meta:
        model = Like
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Like.objects.all(),
                fields=['post', 'user']
            )
        ]
