from django.db.models.signals import post_save, pre_delete, pre_save
from django.db.models.functions import Lower
from django.contrib.auth.models import User
from taggit.models import Tag
from django.db.models import Count, Q
from django.dispatch import receiver
import cloudinary

from entries.models import Entry
from .models import Profile

    
# https://dev.to/earthcomfy/django-user-profile-3hik

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
        

    
# @receiver(post_save, sender=User)
# def save_profile(sender, instance, created, **kwargs):
#     if created:
#         instance.profile.save()

# @receiver(pre_delete, sender=Profile)
# def delete_image(sender, instance, **kwargs):
#     print(cloudinary.uploader.destroy(instance.pic.public_id, invalidate=True))

# @receiver(pre_delete, sender=Entry)
# def delete_link(sender, instance, **kwargs):
#     print('deleting')
#     print(instance)
#     print(cloudinary.uploader.destroy(instance.audio_file.public_id, resource_type = "video", invalidate=True))



# @receiver(post_save, sender=User)
# def update_username_list(sender, instance, created, **kwargs):
#     if created:
#         #current_usernames.append(instance.username)
#         print('signals')

        
# @receiver(post_save, sender=Tag)
# def update_username_list(sender, instance, created, **kwargs):
#     if created:

#         pass


# @receiver(pre_delete, sender=Like)
# def delete_like(sender, instance, **kwargs):
#     if instance.entry.likes > 0:
#         instance.entry.likes -= 1
#         instance.entry.save()
