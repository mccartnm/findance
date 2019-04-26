from django.contrib import admin

from .models import Asset, AssetOwnership

admin.site.register(Asset)
admin.site.register(AssetOwnership)
