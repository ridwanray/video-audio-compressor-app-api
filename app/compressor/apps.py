from django.apps import AppConfig


class CompressorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'compressor'

    def ready(self) -> None:
        import compressor.signals
