from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from taggit.managers import TaggableManager
#from django.template.defaultfilters import slugify
from django.utils.text import slugify
import cloudinary
from unidecode import unidecode

STATUS = ((0, "Private"), (1, "Published"))

# Create your models here.
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
    tag_list = models.CharField(max_length=500, blank=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
   # likes = models.IntegerField(null=True, default=0)
   # liked_users = models.ManyToManyField(User, through=Like, related_name='liked_entries', blank=True)
    publish = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_on"]

    # def created_date(self):
    #     ''' Convert DateTime to pure Date '''
    #     return self.created_on.date()


    def __str__(self):
        return f"{self.title} created by {self.author}"
    
    def save(self, *args, **kwargs):
        # TODO: Check if author already used same title in form in JS file
        #if not self.slug:
        new_slug = f'{self.title}-{self.author.username}'
       # print(new_slug)
        self.slug = slugify(unidecode(new_slug))
        return super(Entry, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        print('Trying to delete')
        print(cloudinary.uploader.destroy(self.audio_file.public_id, resource_type = "video", invalidate=True))
        for id, file in self.old_files.items():
            print(cloudinary.uploader.destroy(id, resource_type = "video", invalidate=True))
        return super().delete(*args, **kwargs)