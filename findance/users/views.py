from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets
from .models import FindanceUser
from .serializers import UserSerializer

class UsersAPI(viewsets.ViewSet):
    """
    View for getting and controlling currencies
    """
    def _get_user(self, pk):
        """
        Obtain a user though the id or code
        """
        kwargs = {}
        try:
            kwargs["pk"] = int(pk)
        except Exception as e:
            kwargs["username__iexact"] = pk
        return get_object_or_404(FindanceUser.objects.all(), **kwargs)

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
        General GET request to retrieving any amount of information for
        findance users.
        :param request: The HttpRequest object django hands us
        :return Response:
        """
        get_data = request.GET

        if 'username' in get_data:
            currencies = FindanceUser.objects.filter(username__iexact=get_data['username'])
            if not currencies.exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            currencies = FindanceUser.objects.all()

        serializer = UserSerializer(currencies, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, format=None):
        """
        Lookup a single user by it's code rather than id
        """
        user = self._get_user(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def create(self, request, format=None):
        """
        Create a FindanceUser
        """
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            new_user = FindanceUser.objects.create(**serializer.validated_data)
            return Response(
                serializer.validated_data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None, format=None):
        """
        Update a given user by code or id
        """
        user = self._get_user(pk)
        serializer = USerSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(user).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
