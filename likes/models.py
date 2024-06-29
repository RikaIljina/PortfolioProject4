"""
models.py for the 'Likes' app.

This module contains the model for the 'Like' object, which tracks user likes
on entries.
"""

from django.db import models
from django.contrib.auth.models import User

from entries.models import Entry


class Like(models.Model):
    """
    A model representing a like given by a user to an entry.

    Attributes:
        user (ForeignKey): The user who liked the entry.
        entry (ForeignKey): The entry being liked.
        created_on (datetime): The date and time when the entry was liked.

    Meta:
        ordering: Specifies the default order of entries.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="liked"
    )
    entry = models.ForeignKey(
        Entry, on_delete=models.CASCADE, related_name="all_likes"
    )
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def save(self, *args, **kwargs):
        """
        Check if the like is valid before saving

        This method ensures that a user cannot like an entry twice and cannot
        like their own entry. If the like is valid, it is saved to the database.
        """
        
        if self.entry.author == self.user:
            return
        else:
            self.entry.save()
            super(Like, self).save(*args, **kwargs)

    def __str__(self):
        """
        Return a string representation of the Like instance

        Returns:
            str: The title of the liked entry and the username of the user.
        """

        return f"Entry {self.entry} liked by {self.user}"
