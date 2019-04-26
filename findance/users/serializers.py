
from rest_framework import serializers
from .models import FindanceUser

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the Currency type
    """
    class Meta:
        model = FindanceUser
        fields = ('id', 'username')

