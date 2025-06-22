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
    PAYMENT_METHOD_CHOICES = [("cash", "Оплата наличными"), ("transfer", "Перевод на счёт")]
    PAYMENT_STATUS_CHOICES = [
        ("pending", "Ожидает оплаты"),
        ("paid", "Оплачен"),
        ("failed", "Ошибка оплаты"),
    ]

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
    payment_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Сумма оплаты"
    )
    payment_methods = models.CharField(
        max_length=8,
        choices=PAYMENT_METHOD_CHOICES,
        default="transfer",
        verbose_name="Метод оплаты",
        help_text="Выберете метод оплаты",
    )
    payment_status = models.CharField(
        max_length=8,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending",
        verbose_name="Статус оплаты",
        help_text="Выберете статус оплаты",
    )

    session_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Id сессии", help_text="Укажите Id сессии"
    )
    link = models.URLField(
        max_length=500, blank=True, null=True, verbose_name="Ссылка на оплату", help_text="Укажите ссылку на оплату"
    )

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Платеж {self.user.email} от {self.payment_date} на сумму {self.payment_amount}"
