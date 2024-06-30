"""
models.py for the 'Mainpage' app.

This module contains the MessageToAdmin model class, which stores all messages
submitted by authenticated users to be read by the admin.
"""

from django.db import models
from django.contrib.auth.models import User


class MessageToAdmin(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="admin_messages"
    )
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=5000)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        """
        Return a string representation of the MessageToAdmin instance

        Returns:
            str: The message subject and the username of the sender.
        """

        return f"Message {self.subject} by {self.user}"
