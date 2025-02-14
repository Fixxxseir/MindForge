from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from config import settings
from lms.models import Course, Lesson


class User(AbstractUser):
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name="Username")
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(
        upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватар", help_text="Загрузите свой аватар"
    )
    phone_number = PhoneNumberField(blank=True, null=True, verbose_name="Телефон")
    country = models.CharField(
        blank=True, null=True, max_length=20, verbose_name="Страна проживания", help_text="Введите страну проживания"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    class Method(models.IntegerChoices):
        CASH = 0, "Наличные"
        TRANSFER = 1, "Перевод на счёт"

    class Status(models.IntegerChoices):
        PENDING = 0, "Ожидает оплаты"
        PAID = 1, "Оплачен"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="payments"
    )
    payment_date = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="оплаченный курс",
        related_name="payments",
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="оплаченный урок",
        related_name="payments",
    )
    payment_amount = models.FloatField(blank=True, null=True, verbose_name="Сумма оплаты")
    payment_methods = models.SmallIntegerField(
        choices=Method.choices, blank=True, null=True, verbose_name="Способ оплаты"
    )
    payment_status = models.SmallIntegerField(
        choices=Status.choices, default=Status.PENDING, verbose_name="Статус оплаты"
    )

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Платеж {self.user.email} от {self.payment_date} на сумму {self.payment_amount}"
