from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    last_request_date = models.DateTimeField(null=True)


class Post(models.Model):
    title = models.CharField(blank=False, max_length=100)
    body = models.CharField(blank=False, max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique user likes')
        ]

    def __str__(self):
        return f'{self.user.username} liked {self.post.title}'
