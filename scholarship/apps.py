from django.apps import AppConfig


class ScholarshipConfig(AppConfig):
    name = 'scholarship'

    def ready(self):
        # Ensure signals are registered when app is ready
        import scholarship.signals  # noqa: F401
