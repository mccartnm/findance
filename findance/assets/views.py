from django.shortcuts import render
from django.shortcuts import get_object_or_404

from findance import abstract
from .models import Asset, AssetOwnership
from .serializers import AssetSerializer, AssetOwnershipSerializer

class AssetAPI(abstract.BaseFindanceAPI):
    serializer = AssetSerializer
    search_alternate = 'name'

class AssetOwnershipAPI(abstract.BaseFindanceAPI):
    serializer = AssetOwnershipSerializer
    search_alternate = None # For the moment
