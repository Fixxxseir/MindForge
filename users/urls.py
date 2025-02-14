from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig

from .views import UserProfileUpdateView, UserRegisterAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="register"),
    path("profile/", UserProfileUpdateView.as_view(), name="profile"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # Получение JWT-токена
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # Обновление JWT-токена
]
