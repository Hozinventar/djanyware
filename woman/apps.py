from django.apps import AppConfig


class WomanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'woman'
    verbose_name = "Женьщины мира"  # в админке показывает называние приложения
