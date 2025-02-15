from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer, UserProfileSerializer, UserRegisterSerializer, UserDetailSerializer

User = get_user_model()


class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
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


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = (
        "paid_course",
        "paid_lesson",
        "payment_methods",
    )
    ordering_fields = ("payment_date",)
