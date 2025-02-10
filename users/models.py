from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name="Username")
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(
        upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватар", help_text="Загрузите свой аватар"
    )
    phone_number = PhoneNumberField(blank=True, verbose_name="Телефон")
    country = models.CharField(blank=True, max_length=20, verbose_name="Страна проживания", help_text="Введите страну проживания")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
