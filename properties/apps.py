# properties/apps.py

from django.apps import AppConfig

class PropertiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "properties"

    def ready(self):
        # Import signals so they are registered
        try:
            import properties.signals  # noqa: F401
        except Exception:
            # swallow import errors during some management commands or tests
            pass
