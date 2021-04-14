from django.urls import path
from users.views import SignUpView, activate

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
]