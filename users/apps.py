from django.apps import AppConfig
#from .utils import get_username_list


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals
        #get_username_list()
        