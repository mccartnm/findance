from django.shortcuts import render
from django.shortcuts import get_object_or_404

# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from rest_framework.response import Response
# from rest_framework import viewsets
from findance import abstract
from .models import Currency
from .serializers import CurrencySerializer

class CurrencyAPI(abstract.BaseFindanceAPI):
    serializer = CurrencySerializer
    search_alternate = 'code'
