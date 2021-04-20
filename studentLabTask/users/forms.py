from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, required=True, help_text='Required')
    first_name = forms.CharField(max_length=40, required=True, help_text='Required')
    last_name = forms.CharField(max_length=40, required=True, help_text='Required')
    birthday = forms.CharField()

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'birthday',
                  'first_name',
                  'last_name')


class UserEditForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'birthday',
                  'first_name',
                  'last_name')


