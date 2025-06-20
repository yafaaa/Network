from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)  # Add this line

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"
