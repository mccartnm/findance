from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Currency
from .serializers import CurrencySerializer

class CurrenyAPI(viewsets.ViewSet):
    """
    View for getting and controlling currencies
    """
    def _get_currency(self, pk):
        """
        Obtain a currency though the id or code
        """
        kwargs = {}
        try:
            kwargs["pk"] = int(pk)
        except Exception as e:
            kwargs["code__iexact"] = pk
        return get_object_or_404(Currency.objects.all(), **kwargs)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request, format=None):
        """
        General GET request to retrieving any amounf of information for
        findance.
        :param request: The HttpRequest object django hands us
        :return Response:
        """
        get_data = request.GET

        if 'code' in get_data:
            currencies = Currency.objects.filter(code__iexact=get_data['code'])
            if not currencies.exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            currencies = Currency.objects.all()

        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, format=None):
        """
        Lookup a single currency by it's code rather than id
        """
        currency = self._get_currency(pk)
        serializer = CurrencySerializer(currency)
        return Response(serializer.data)

    def create(self, request, format=None):
        """
        Create a Currency
        """
        serializer = CurrencySerializer(data=request.data)

        if serializer.is_valid():
            new_currency = Currency.objects.create(**serializer.validated_data)
            return Response(
                serializer.validated_data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None, format=None):
        """
        Update a given currency by code or id
        """
        currency = self._get_currency(pk)
        serializer = CurrencySerializer(currency, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(CurrencySerializer(currency).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
