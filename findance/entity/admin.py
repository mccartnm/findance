from django.contrib import admin

from .models import OwningEntity, EntityControl

admin.site.register(OwningEntity)
admin.site.register(EntityControl)
