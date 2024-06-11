from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from taggit.managers import TaggableManager
#from django.template.defaultfilters import slugify
from django.utils.text import slugify
import cloudinary
from unidecode import unidecode
from entries.models import Entry

class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter")
    entry = models.ForeignKey(
        Entry, on_delete=models.CASCADE, related_name="all_comments")
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return (f"{self.author} commented on {self.entry}: " +
                f"{self.content[:15]}...")
