from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import FindanceUser

class FindanceUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = FindanceUser
        fields = ('username', 'email', 'is_staff', 'is_superuser')

class FindanceUserChangeForm(UserChangeForm):

    class Meta:
        model = FindanceUser
        fields = ('username', 'email', 'is_staff', 'is_superuser')