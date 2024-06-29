from django.db import models
from django.contrib.auth.models import User
import cloudinary
from cloudinary.models import CloudinaryField


# Create your models here.


class Profile(models.Model):
    """User profile
    Must be created automatically when user registers
    Move to separate "users" app?"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    # TODO: limit image size
    pic = CloudinaryField("image", default="placeholder")
    joined = models.DateTimeField(auto_now_add=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    spotify = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self) -> str:
        return f"User profile of {self.user.username}"

    def delete(self, *args, **kwargs):
        print("Trying to delete")
        print(cloudinary.uploader.destroy(self.pic.public_id, invalidate=True))
        return super().delete(*args, **kwargs)
