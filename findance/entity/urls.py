
from django.urls import path, include
from .views import OwningEntityAPI, EntityControlAPI

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('entity', OwningEntityAPI, basename='owningentity')
router.register('control', EntityControlAPI, basename='entitycontrol')

urlpatterns = []
urlpatterns += router.urls
