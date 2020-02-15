from django.contrib.auth import get_user_model
from django.db import models

from apps.post.models import Post


class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name='likes', on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ['post', 'user']

    def __str__(self):
        return f'{self.post.title} {self.user.email}'
