from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import UserProfileSerializer

User = get_user_model()


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
