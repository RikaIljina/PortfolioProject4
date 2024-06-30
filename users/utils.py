"""
utils.py for the 'Users' app

This module contains user-related functions that are used by the views.

get_all_usernames(): Creates a dict with all current usernames and profile
    picture URLs
"""

from django.contrib.auth.models import User


def get_all_usernames():
    """
    Creates a dict with all current usernames and profile picture URLs

    This function creates a dictionary containing all usernames and their
    profile picture links. The dictionary is sorted alphabetically by username.

    Returns:
        dict: A dictionary with usernames as key and links to the profile
            picture as value.
    """

    all_users = User.objects.select_related("profile")

    current_users = dict(
        {value.username: value.profile.pic.url for value in all_users}
    )
    users = dict(sorted(current_users.items()))

    return users
