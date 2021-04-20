from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class DateInput(forms.DateInput):
    input_type = 'date'


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, required=True, help_text='Required')
    first_name = forms.CharField(max_length=40, required=True, help_text='Required')
    last_name = forms.CharField(max_length=40, required=True, help_text='Required')
    birthday = forms.DateField(widget=DateInput)

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'birthday',
                  'first_name',
                  'last_name')


class UserEditForm(UserChangeForm):
    email = forms.EmailField(max_length=200, required=True, help_text='Required')

    class Meta:
        model = User
        fields = ('username',
                  'email')


