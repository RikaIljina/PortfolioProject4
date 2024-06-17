from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from taggit.managers import TaggableManager
from taggit.models import Tag
from unidecode import unidecode
from cloudinary.models import CloudinaryField

import cloudinary


STATUS = ((0, "Private"), (1, "Published"))

class Entry(models.Model):
    """
    A model representing an audio entry created by a user.

    Attributes:
        author (ForeignKey): The user who created the entry.
        title (str): The title of the entry.
        created_on (datetime): The date and time when the entry was created.
        updated_on (datetime): The date and time when the entry was last
            updated.
        audio_file (CloudinaryField): The audio file associated with the entry,
            stored on Cloudinary.
        old_files (JSONField): A JSON field to store previous versions of the
            audio file.
        description (str): A description of the entry.
        tags (TaggableManager): Tags associated with the entry for
            categorization.
        slug (SlugField): A slugified version of the title and author username
            for URL use.
        publish (int): The publication status of the entry (0 for Private, 1
            for Published).

    Meta:
        ordering: Specifies the default order of entries.
    """

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="all_entries")
    title = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    audio_file = CloudinaryField('video', resource_type='auto', format='mp3')
    old_files = models.JSONField(default=dict, blank=True)
    description = models.TextField()
    tags = TaggableManager(verbose_name='Tags')
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    publish = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_on"]


    def __str__(self):
        """
        Return a string representation of the Entry instance

        Returns:
            str: The title of the entry and the username of the author.
        """
        
        return f"{self.title} created by {self.author}"


    def save(self, *args, **kwargs):
        """
        Override the save method to handle tag cleanup

        This method deletes tags that are no longer used by any entry.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        # new_slug = f'{self.title}-{self.author.username}'
        # # unidecode is needed to process non-latin titles
        # self.slug = slugify(unidecode(new_slug))
        # if self.__class__.objects.filter(slug=self.slug).exists():
        #     print('Error!')
        #     raise ValidationError('Please choose a different title to make'
        #                           'sure the entry slug is unique.')
        # else:
        #     print('Unique slug')
        # Delete tags that are no longer used by any entry
        Tag.objects.filter(entry=None).delete()
        
        return super(Entry, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        """
        Override the delete method to handle tag and file cleanup

        This method deletes tags that are no longer used by any entry.
        The method also ensures that the main audio file as well as all
        previous versions of the file are deleted from Cloudinary storage.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        
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