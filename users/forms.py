"""Related to user forms"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User


class DateInput(forms.DateInput):
    """Date form field"""
    input_type = 'date'


class BaseUserForm(forms.Form):
    """Base user form"""
    unconfirmed_email = forms.EmailField(max_length=200,
                                         required=True,
                                         help_text='Required')
    first_name = forms.CharField(max_length=40,
                                 required=True,
                                 help_text='Required')
    last_name = forms.CharField(max_length=40,
                                required=True,
                                help_text='Required')
    birthday = forms.DateField(widget=DateInput,
                               required=False)


class SignupForm(UserCreationForm, BaseUserForm):
    """Signup form"""
    class Meta:
        model = User
        fields = ('username',
                  'unconfirmed_email',
                  'birthday',
                  'first_name',
                  'last_name')


class UserEditForm(UserChangeForm, BaseUserForm):
    """User edit form"""
    class Meta:
        model = User
        fields = ('username',
                  'unconfirmed_email',
                  'birthday',
                  'first_name',
                  'last_name')
