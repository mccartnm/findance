
from rest_framework import serializers

from findance import abstract
from users.serializers import UserSerializer
from .models import OwningEntity, EntityControl

class OwningEntitySerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the OwningEntity objects
    """
    class Meta:
        model = OwningEntity
        fields = ('id', 'url', 'name')#, 'assets')


class EntityControlSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the EntityControl objects
    """
    user = UserSerializer()
    entity = OwningEntitySerializer()

    class Meta:
        model = EntityControl
        fields = ('id', 'url', 'user', 'entity', 'permission')