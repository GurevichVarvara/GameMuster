from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.views.generic import CreateView

from users.tokens import EmailConfirmationTokenGenerator
from users.forms import SignupForm


class SignUpView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            logout(self.request)

        user = form.save(commit=False)

        # Don't let user to login before email confirmation
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
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

        return render(self.request, 'users/base_message.html',
                      {'message': 'Please confirm your email address '
                                  'to complete the registration'})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None

    if user is not None \
            and EmailConfirmationTokenGenerator().check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return HttpResponse('Activation link is invalid!')


def profile(request):
    return render(request, 'users/profile.html')



