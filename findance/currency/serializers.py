
from rest_framework import serializers
from .models import Currency

class CurrencySerializer(serializers.ModelSerializer):
    """
    Serializer for the Currency type
    """
    class Meta:
        model = Currency
        fields = ('id', 'code', 'fullname', 'rate')

