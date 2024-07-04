"""
models.py for the 'Entries' app.

This module contains the Entry model class, which stores all entry-related
data in the database.
"""

from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
import cloudinary
from cloudinary.models import CloudinaryField


class Entry(models.Model):
    """
    A model representing an audio entry created by a user.

    Attributes:
        STATUS (tuple): Choices for the IntegerField to indicate whether the
            entry is private or public.
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

    Methods:
        delete(): Override the delete method to handle file cleanup.
    """

    STATUS = ((0, "Private"), (1, "Published"))

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="all_entries"
    )
    title = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    audio_file = CloudinaryField("video", resource_type="auto", format="mp3")
    old_files = models.JSONField(default=dict, blank=True)
    description = models.TextField()
    tags = TaggableManager(verbose_name="Tags")
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    publish = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} created by {self.author}"

    def delete(self, *args, **kwargs):
        """
        Override the delete method to handle file cleanup

        This method ensures that the main audio file as well as all
        previous versions of the file are deleted from Cloudinary storage.
        """

        # Destroy unused Cloudinary files
        # The response could be used to send an error message to the admin
        # if the file couldn't be destroyed
        cl_response = cloudinary.uploader.destroy(
            self.audio_file.public_id,
            resource_type="video",
            invalidate=True,
        )
        for id in self.old_files.keys():
            cl_response = cloudinary.uploader.destroy(
                    id, resource_type="video", invalidate=True
                )

        return super().delete(*args, **kwargs)
