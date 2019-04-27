
from rest_framework import serializers
from .models import Currency

class CurrencySerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Currency type
    """
    class Meta:
        model = Currency
        fields = ('id', 'url', 'code', 'fullname', 'rate')

