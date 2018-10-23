from django.apps import AppConfig


class DialogsConfig(AppConfig):
    name = 'dialogs'
    
    def ready(self):
        from dialogs import signals