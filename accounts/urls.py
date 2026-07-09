from django.urls import path
from .views import RegisterView, profile_view, change_password_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile_view, name='profile'),
    path('profile/change-password/', change_password_view, name='change_password'),
]