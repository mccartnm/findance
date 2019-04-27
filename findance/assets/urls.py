
from django.urls import path, include
from .views import AssetAPI, AssetOwnershipAPI

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('asset', AssetAPI, basename='asset')
router.register('assetownership', AssetOwnershipAPI, basename='assetownership')

urlpatterns = []
urlpatterns += router.urls
