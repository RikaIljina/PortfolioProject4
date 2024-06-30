"""
signals.py for the 'Users' app

This module contains signals that fire on certain triggers.

create_profile(): Triggered by creation of User object; creates Profile object
delete_profile_pic(): Triggered by deletion of Profile object; deletes profile
    picture from Cloudinary
"""

from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
import cloudinary

from .models import Profile


# Adapted from https://dev.to/earthcomfy/django-user-profile-3hik
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Automatically create profile after user registration
    
    This function automatically creates a user profile whenever a user is added
    by the admin or registers via the website to ensure that every User object
    is associated with a Profile object containing the placeholder avatar.
    """

    if created:
        Profile.objects.create(user=instance)


@receiver(pre_delete, sender=Profile)
def delete_profile_pic(sender, instance, **kwargs):
    """
    Delete image from Cloudinary when deleting users in bulk
    
    This function is called before a user profile is deleted. It deletes
    the associated profile pic from Cloudinary.
    """
    
    cl_response = cloudinary.uploader.destroy(
        instance.pic.public_id, invalidate=True)
