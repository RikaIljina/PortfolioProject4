from django.db.models.signals import post_save, pre_delete, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile, Like

# https://dev.to/earthcomfy/django-user-profile-3hik

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
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
        print(instance.entry.likes)
        instance.entry.save()
