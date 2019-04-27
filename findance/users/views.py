from django.shortcuts import render
from django.shortcuts import get_object_or_404

from findance import abstract
from .models import FindanceUser
from .serializers import UserSerializer

class UsersAPI(abstract.BaseFindanceAPI):
    """
    View for getting and controlling currencies
    """
    serializer = UserSerializer
    search_alternate = 'username'
    