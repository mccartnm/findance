
from rest_framework import serializers
from .models import FindanceUser

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Currency type
    """
    class Meta:
        model = FindanceUser
        fields = ('id', 'url', 'username', 'email')

