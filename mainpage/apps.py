from django.apps import AppConfig
#from .utils import get_all_tags


class MainpageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainpage'

    def ready(self):
        import mainpage.signals
        #get_all_tags()