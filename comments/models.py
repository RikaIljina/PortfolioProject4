from django.db import models
from django.contrib.auth.models import User

from entries.models import Entry


class Comment(models.Model):
    """Model to store a comment made by a user on an entry.

    Attributes:
        author (ForeignKey): Reference to the user who made the comment.
        entry (ForeignKey): Reference to the entry the comment is associated
                            with.
        content (TextField): The text content of the comment.
        created_on (DateTimeField): The date and time when the comment was
                                    created.
        updated_on (DateTimeField): The date and time when the comment was last
                                    updated.

    Meta:
        ordering (list): Specifies that comments should be ordered by creation
                         date in descending order.

    Methods:
        __str__(): Returns a string representation of the comment.
    """

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter"
    )
    entry = models.ForeignKey(
        Entry, on_delete=models.CASCADE, related_name="all_comments"
    )
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return (
            f"{self.author} commented on {self.entry}: "
            f"{self.content[:15]}..."
        )
