from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=70)
    content = models.TextField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator", default=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


