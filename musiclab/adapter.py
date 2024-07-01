"""
adapter.py for Musiclab project

Extends the functionality of the allauth package
"""

from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError


# https://stackoverflow.com/a/50941366
class UsernameMaxAdapter(DefaultAccountAdapter):
    """
    Modify the username max length validation of allauth

    Methods:
        clean_username(): Check if username exceeds 20 characters
    """

    def clean_username(self, username):
        """
        Check if username exceeds 20 characters

        This method overrides the superclass method to ensure that usernames
        are max 20 characters long.

        Args:
            username (str): Username entered into the login or signup form

        Raises:
            ValidationError: If the username length exceeds 20 characters

        Returns:
            str: The cleaned username
        """

        if len(username) > 20:
            raise ValidationError(
                "Please choose a username with max 20 characters"
            )
        return DefaultAccountAdapter.clean_username(self, username)
