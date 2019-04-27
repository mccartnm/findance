

from django.urls import path, include
from .views import UsersAPI

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', UsersAPI, basename='findanceuser')

urlpatterns = []
urlpatterns += router.urls
