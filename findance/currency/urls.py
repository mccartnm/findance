
from django.urls import path, include
from .views import CurrencyAPI

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('currency', CurrencyAPI, basename='currency')

urlpatterns = []
urlpatterns += router.urls
