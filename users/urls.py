from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig

from .views import PaymentListAPIView, UserListAPIView, UserRegisterAPIView, UserRetrieveUpdateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="register"),
    path("list/", UserListAPIView.as_view(), name="profile"),
    path("profile/", UserRetrieveUpdateAPIView.as_view(), name="profile"),
    path("profile/<int:pk>/", UserRetrieveUpdateAPIView.as_view(), name="profile"),
    path(
        "token/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="token_obtain_pair"
    ),  # Получение JWT-токена / авторизация
    path(
        "token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"
    ),  # Обновление access-JWT-токена через refresh-JWT-токен
    path("payments/", PaymentListAPIView.as_view(), name="user-payment"),
]
