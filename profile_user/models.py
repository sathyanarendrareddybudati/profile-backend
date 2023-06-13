from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=None)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=255)
    profile_picture = models.ImageField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return self.name