

from django.urls import path, include
from .views import UsersAPI

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', UsersAPI, basename='users')

urlpatterns = []
urlpatterns += router.urls
