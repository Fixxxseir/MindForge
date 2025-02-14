from django.urls import path, include
from .views import UserProfileUpdateView
from users.apps import UsersConfig


app_name = UsersConfig.name

urlpatterns = [
    path('edit_profile/', UserProfileUpdateView.as_view(), name='edit_profile'),
]