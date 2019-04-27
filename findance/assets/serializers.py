
from rest_framework import serializers
from .models import Asset, AssetOwnership

from entity.serializers import OwningEntitySerializer

class AssetSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Assets
    """
    class Meta:
        model = Asset
        fields = ('id', 'url', 'name', 'description', 'value')


class AssetOwnershipSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for AssetOwnership objects
    """
    owner = OwningEntitySerializer()
    asset = AssetSerializer()

    class Meta:
        model = AssetOwnership
        fields = ('id', 'url', 'asset', 'owner', 'percentage', 'count')