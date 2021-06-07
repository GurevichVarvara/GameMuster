"""users URL Configuration"""
from django.urls import path
from users.views import SignUpView, activate, profile, UserEditView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('profile/', profile, name='profile'),
    path('profile_edit/<int:pk>', UserEditView.as_view(), name='profile-edit')
]
