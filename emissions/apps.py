from django.apps import AppConfig

app_name = 'emissions'
class EmissionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'emissions'

    def ready(self):
        import emissions.signals 
