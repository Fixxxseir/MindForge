from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer, UserPrivateSerializer, UserPublicSerializer, UserRegisterSerializer

User = get_user_model()


class UserRegisterAPIView(generics.CreateAPIView):
    """Представление регистрации нового пользователя"""

    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """Метод обработки POST-запроса для регистрации пользователя.
        Метод возвращает информацию о созданном пользователе пропущенную через сериалайзер
        для корректной выдачи информации.
        Два токена, access - для авторизации, и refresh - для обновления access токена.
        """
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.save()
        return Response(
            {
                "user": UserRegisterSerializer(tokens["user"]).data,
                "refresh": tokens["refresh"],
                "access": tokens["access"],
            }
        )


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Представление детальной информации и изменения профиля пользователя."""

    queryset = User.objects.all()
    serializer_class = UserPrivateSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        """Если пользователь запрошивает свой профиль используется приватный сериалайзер, если нет, то публичный."""
        if self.request.user == self.get_object():
            return UserPrivateSerializer
        return UserPublicSerializer

    def get_object(self):
        """Логика отдачи объекта, если в запросе pk есть то возвращаем объект по этому pk,
        если нет то возвращаем текущего пользователя"""
        if "pk" in self.kwargs:
            return super().get_object()

        return self.request.user


class UserListAPIView(generics.ListAPIView):
    """Представление для получения списка всех пользователей.
    Используется публичный сериалайзер для публичного использования."""

    queryset = User.objects.all()
    serializer_class = UserPublicSerializer


class PaymentListAPIView(generics.ListAPIView):
    """Представление для получения списка платежей"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = (
        "paid_course",
        "paid_lesson",
        "payment_methods",
    )
    ordering_fields = ("payment_date",)
