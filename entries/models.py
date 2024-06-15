from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from taggit.managers import TaggableManager
from taggit.models import Tag
from unidecode import unidecode
from cloudinary.models import CloudinaryField
import cloudinary


STATUS = ((0, "Private"), (1, "Published"))

class Entry(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="all_entries")
    title = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    audio_file = CloudinaryField('raw', resource_type='auto', format='mp3')
    old_files = models.JSONField(default=dict, blank=True)
    description = models.TextField()
    tags = TaggableManager(verbose_name='Tags')
   # tag_list = models.CharField(max_length=500, blank=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    publish = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_on"]


    def __str__(self):
        return f"{self.title} created by {self.author}"


    def save(self, *args, **kwargs):
        new_slug = f'{self.title}-{self.author.username}'
        # unidecode is needed to process non-latin titles
        self.slug = slugify(unidecode(new_slug))
        # Delete tags that are no longer used by any entry
        Tag.objects.filter(entry=None).delete()
        
        return super(Entry, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        # Delete tags that are no longer used by any entry
        Tag.objects.filter(entry=None).delete()
        # Destroy unused Cloudinary files
        print(cloudinary.uploader.destroy(
            self.audio_file.public_id, resource_type = "video",
            invalidate=True))
        for id, file in self.old_files.items():
            print(cloudinary.uploader.destroy(
                id, resource_type = "video", invalidate=True))
            
        return super().delete(*args, **kwargs)