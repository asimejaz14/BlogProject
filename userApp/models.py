from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(default=timezone.now, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='userApp/profile_pics/', default='userApp/f_tJS8NNw.png', null=True)

    def __str__(self):
        return 'Profile ' + self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_image.path)
        if img.width > 300 or img.height > 300:
            output_img = (300, 300)
            img.thumbnail(output_img)
            img.save(self.profile_image.path)
