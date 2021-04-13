from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from users.forms import SignupForm

class SignUpView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
