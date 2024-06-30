"""
signals.py for the 'Mainpage' app

This module contains signals that fire on certain triggers.

delete_tags(): Triggered by the deletion of the Entry object; deletes all tags
    with no associated entries. 
"""

from django.db.models.signals import post_delete
from django.dispatch import receiver
from taggit.models import Tag

from entries.models import Entry


@receiver(post_delete, sender=Entry)
def delete_tags(sender, instance, **kwargs):
    """
    Deletes all tags with no associated entries 
    
    This function is triggered when an entry has been deleted. It queries the
    Tag model to find tags with no associated entries and deletes them.
    """

    Tag.objects.filter(entry=None).delete()
