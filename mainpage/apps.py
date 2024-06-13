from django.apps import AppConfig


class MainpageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainpage'

    def ready(self):
        import mainpage.signals
        from .utils import get_all_tags, delete_tags
        delete_tags()
        get_all_tags() 