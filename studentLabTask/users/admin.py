from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import SignupForm, UserEditForm


class CustomUserAdmin(UserAdmin):
    add_form = SignupForm
    form = UserEditForm
    model = User
    list_display = ['username',
                    'email',
                    'birthday',
                    'first_name',
                    'last_name']


admin.site.register(User, CustomUserAdmin)