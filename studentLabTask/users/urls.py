from django.urls import path
from users.views import SignUpView, activate, profile

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('profile/', profile, name='profile')
]