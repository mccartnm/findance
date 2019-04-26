

from django.urls import path, include
from .views import CurrenyAPI

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', CurrenyAPI, basename='currency')

urlpatterns = []
urlpatterns += router.urls
