from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='posts')
    title = models.CharField(max_length=50, unique=True)
    text = models.TextField(max_length=5000)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'
