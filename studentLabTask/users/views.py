from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.views.generic import CreateView

from users.tokens import EmailConfirmationTokenGenerator
from users.forms import SignupForm


def send_confirmation_email(request, form):
    user = form.save(commit=False)

    # Don't let user to login before email confirmation
    user.is_active = False

    # Save user to database


    current_site = get_current_site(request)
    send_mail(
        subject='Email confirmation',
        message=render_to_string('users/account_activation.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': EmailConfirmationTokenGenerator().make_token(user),
        }),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )

    return HttpResponse('Please confirm your email address to complete the registration')


class SignUpView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        return send_confirmation_email(self.request, form)


def activate(request, uidb64, token):
    print('Yesss')
