# https://stackoverflow.com/a/50941366

from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError

class UsernameMaxAdapter(DefaultAccountAdapter):

    def clean_username(self, username):
        if len(username) > 20:
            raise ValidationError(
                'Please choose a username with max 20 characters')
        return DefaultAccountAdapter.clean_username(self, username)