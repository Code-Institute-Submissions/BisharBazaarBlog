from django.apps import AppConfig
from django.contrib import admin
from .models import Product

admin.site.register(Product)


class BlogConfig(AppConfig):
    """
    Provides primary key type for BazaarApp app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BazaarApp'