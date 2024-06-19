from django.db.models.signals import post_save, pre_delete, pre_save, post_delete
from django.db.models.functions import Lower
from django.contrib.auth.models import User
from taggit.models import Tag
from django.db.models import Count, Q
from django.dispatch import receiver
import cloudinary
from .utils import get_all_tags
from entries.models import Entry

    

@receiver(post_save, sender=Tag)
def create_tag(sender, instance, created, **kwargs):
    print('new tag created, signals')
    #Tag.objects.filter(entry=None).delete()
    
    get_all_tags()


@receiver(post_delete, sender=Tag)
def del_tag(sender, instance, **kwargs):
   # Tag.objects.filter(entry=None).delete()
    
    get_all_tags()


@receiver(post_save, sender=Entry)
def check_tags(sender, instance, created, **kwargs):
    print('entry saved created, signals')
    #Tag.objects.filter(entry=None).delete()
    
    get_all_tags()

@receiver(post_delete, sender=Entry)
def delete_tags(sender, instance, **kwargs):
    #Tag.objects.filter(entry=None).delete()
    
    get_all_tags()

    
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