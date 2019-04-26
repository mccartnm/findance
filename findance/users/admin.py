from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import FindanceUserCreationForm, FindanceUserChangeForm
from .models import FindanceUser

class FindanceUserAdmin(UserAdmin):
    add_form = FindanceUserCreationForm
    form = FindanceUserChangeForm
    model = FindanceUser
    list_display = ['email', 'username', 'is_staff', 'is_superuser']

admin.site.register(FindanceUser, FindanceUserAdmin)