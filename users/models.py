"""
models.py for the 'Users' app.

This module contains the Profile model class, which stores all profile data
for a specific registered user in the database.
"""

from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    """
    A model representing a user profile.

    Attributes:
        user (ForeignKey): The user whom the profile belongs to.
        bio (str): A text with info about the user.
        joined (datetime): The date and time when the user joined the website.
        facebook, twitter,
        instagram, youtube,
        spotify (str): URLs to the social network pages the user provided.
        website (str): URL to a website the user provided.
        email (str): Email address the user provided.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
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
