from django.db import models
from post.models import Post
from django.contrib.auth.models import User

# Create your models here.

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", default=1)

    comment = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.post.title} {self.comment}"