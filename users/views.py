from django.contrib.auth import login, logout
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.views.generic import CreateView, UpdateView
from datetime import datetime
from django.contrib.auth.decorators import login_required

from users.tokens import EmailConfirmationTokenGenerator
from users.forms import SignupForm, UserEditForm


def send_confirmation_email(request, user, email):
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
        recipient_list=[email],
        fail_silently=False,
    )


def update_user_with_email(request, form, message):
    user = form.save()

    user.save()

    send_confirmation_email(request, user, user.unconfirmed_email)

    return render(request, 'users/message.html',
                  {'message': message})


class SignUpView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        return update_user_with_email(self.request,
                                      form,
                                      'Please confirm your email address '
                                      'to complete the registration')


def is_user_email_changed(prev_email, form):
    current_email = form['email'].value()

    return current_email.lower() != prev_email.lower()


class UserEditView(UpdateView):
    form_class = UserEditForm
    model = User
    success_url = reverse_lazy('profile')
    template_name = 'users/user_update_form.html'

    def form_valid(self, form):
        if is_user_email_changed(self.get_object().email,
                                 form):
            response = update_user_with_email(self.request,
                                              form,
                                              'Please confirm your '
                                              'new email address')
        else:
            response = super(UserEditView, self).form_valid(form)

        return response


def activate(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.filter(pk=uid).first()

    if not (user and EmailConfirmationTokenGenerator().check_token(user, token)):
        return HttpResponse('Activation link is invalid!')

    user.active_time = datetime.now()
    user.email = user.unconfirmed_email
    user.unconfirmed_email = None
    user.save()
    login(request, user)
    return redirect('index')


@login_required
def profile(request):
    return render(request, 'users/profile.html')
