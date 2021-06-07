"""Admin configuration module"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import SignupForm, UserEditForm


class CustomUserAdmin(UserAdmin):
    """Describe how to represent user objects on admin page"""
    add_form = SignupForm
    form = UserEditForm
    model = User
    list_display = ['username',
                    'email',
                    'birthday',
                    'first_name',
                    'last_name',
                    'active_time']


admin.site.register(User, CustomUserAdmin)
