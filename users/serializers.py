from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from lms.models import Course, Lesson
from users.models import Payment

User = get_user_model()



class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "avatar", "phone_number", "country"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            avatar=validated_data.get("avatar", None),
            phone_number=validated_data.get("phone_number", None),
            country=validated_data.get("country", None),
        )
        refresh = RefreshToken.for_user(user)
        return {
            "user": user,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class PaymentSerializer(serializers.ModelSerializer):
    paid_course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=False)
    paid_lesson = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all(), required=False)
    paid_course_title = serializers.SerializerMethodField()
    paid_lesson_title = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ("user", "payment_status", "session_id", "link")

    def get_paid_course_title(self, obj):
        if obj.paid_course:
            return obj.paid_course.title
        return "Не приобретено"

    def get_paid_lesson_title(self, obj):
        if obj.paid_lesson:
            return obj.paid_lesson.title
        return "Не приобретено"


class UserPrivateSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "avatar", "phone_number", "country", "payments"]
        read_only_fields = [
            "id",
            "payments",
        ]


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "avatar", "phone_number", "country"]
        read_only_fields = fields
