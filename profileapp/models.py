

from django.db import models
from django.contrib.auth.models import User

class Profileapp(models.Model):
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    profile_photo = models.ImageField(default='profile_images\default.jpg', upload_to='profile_images/')

  

    def __str__(self):
        return self.user.username
