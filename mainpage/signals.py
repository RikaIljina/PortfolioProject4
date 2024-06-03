from django.db.models.signals import post_save, pre_delete, pre_save
from django.db.models.functions import Lower
from django.contrib.auth.models import User
from taggit.models import Tag
from django.db.models import Count, Q
from django.dispatch import receiver

from .models import Profile, Like

# Global lists that store querysets to be used by all views
current_usernames = []

    
# https://dev.to/earthcomfy/django-user-profile-3hik

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        current_usernames.append(instance.username)

    
@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        instance.profile.save()


# @receiver(pre_save, sender=Like)
# def check_like(sender, instance, **kwargs):
#     #print(instance.user.liked.all())
#     for like in instance.user.liked.all().filter(entry=instance.entry.id):
#         print(like.entry.id)
#     if instance.user.liked.all().filter(entry=instance.entry.id).count() != 0:
#         print('Signal: You already liked it')
#         return
#     print(instance.entry)
#     #print(instance.entry.all_likes.all())
    

# @receiver(post_save, sender=Like)
# def create_like(sender, instance, created, **kwargs):
#     if created:
#         instance.entry.likes += 1
#         print(instance.entry.likes)
#         instance.entry.save()


@receiver(pre_delete, sender=Like)
def delete_like(sender, instance, **kwargs):
    if instance.entry.likes > 0:
        instance.entry.likes -= 1
        instance.entry.save()
