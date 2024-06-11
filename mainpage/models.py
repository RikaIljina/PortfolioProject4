from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from taggit.managers import TaggableManager
#from django.template.defaultfilters import slugify
from django.utils.text import slugify
import cloudinary
from unidecode import unidecode
from entries.models import Entry


# Create your models here.


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="liked")
    entry = models.ForeignKey(
        Entry, on_delete=models.CASCADE, related_name="all_likes")
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]


    def save(self, *args, **kwargs):
        '''Checks if the like is valid before saving
        This makes sure that a user cannot like an entry twice and cannot
        like their own entry
        '''
        if self.user.liked.all().filter(entry=self.entry.id).count() != 0 \
            or self.entry.author == self.user:
            print('You already liked it or this is your own entry')
            return
        else:
           # self.entry.likes = self.entry.all_likes.count() + 1
            self.entry.save()
            super(Like, self).save(*args, **kwargs)

    def __str__(self):
        return f"Entry {self.entry} liked by {self.user}"
