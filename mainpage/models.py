"""
models.py for the 'Mainpage' app.

This module contains the MessageToAdmin model class, which stores all messages
submitted by authenticated users to be read by the admin.
"""

from django.db import models
from django.contrib.auth.models import User


class MessageToAdmin(models.Model):
    """
    A model representing a message.

    Attributes:
        user (ForeignKey): The user submitting the message.
        subject (str): The subject of the message.
        message (str): The text content of the message.
        created_on (datetime): The date and time when the message was sent.

    Meta:
        ordering: Specifies the default order of entries.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="admin_messages"
    )
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=5000)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Message {self.subject} by {self.user}"
