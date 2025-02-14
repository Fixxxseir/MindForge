from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import connection
from phonenumber_field.phonenumber import PhoneNumber

from lms.models import Course, Lesson
from users.models import Payment

User = get_user_model()


class Command(BaseCommand):
    help = "Создаёт нового пользователя"

    def reset_auto_increment(self):
        """Очищает таблицы Course, Lesson, Payment и сбрасывает счётчики автоинкремента."""
        with connection.cursor() as cursor:

            cursor.execute("TRUNCATE TABLE lms_course RESTART IDENTITY CASCADE;")

            cursor.execute("TRUNCATE TABLE lms_lesson RESTART IDENTITY CASCADE;")

            cursor.execute("TRUNCATE TABLE users_payment RESTART IDENTITY CASCADE;")

            self.stdout.write(self.style.SUCCESS("Очищены таблицы Course, Lesson и Payment и счётчики ID сброшены."))

    # Создание Юзера
    def handle(self, *args, **kwargs):
        self.reset_auto_increment()
        email = input("Введите email: ")
        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(f"Пользователь с email {email} уже существует!"))
            return

        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
        )

        self.stdout.write(self.style.SUCCESS(f"Пользователь {user.email} успешно создан!"))
        # Создание курсов
        courses = [
            {
                "title": "Курс по Python",
                "description": "полный курс по Python",
            },
            {
                "title": "Курс по Java",
                "description": "Полный курс по Java",
            },
            {
                "title": "Курс по golang",
                "description": "Полный курс по golang",
            },
        ]
        for course_data in courses:
            course, created = Course.objects.get_or_create(**course_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Добавление успешно {course.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Что-то пошло не так"))
        # Создание урок
        lessons = [
            {
                "course": Course.objects.get(id=1),
                "title": "Азы Python",
                "description": "Введение",
            },
            {
                "course": Course.objects.get(id=2),
                "title": "Азы java",
                "description": "Введение",
            },
            {
                "course": Course.objects.get(id=3),
                "title": "Азы golang",
                "description": "Введение",
            },
            {
                "course": Course.objects.get(id=1),
                "title": "Типы данных Python",
                "description": "Информация о том какие бывают данные в языке Python",
            },
        ]
        for lesson_data in lessons:
            lesson, created = Lesson.objects.get_or_create(**lesson_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Добавление успешно {lesson.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Что-то пошло не так"))
        # Создание платежей
        payments = [
            {
                "user": user,
                "paid_course": Course.objects.get(id=1),
                "payment_amount": 10000.0,
                "payment_methods": 0,
                "payment_status": 1,
            },
            {"user": user, "paid_course": Course.objects.get(id=3), "payment_amount": 123123.0, "payment_status": 0},
            {
                "user": user,
                "paid_lesson": Lesson.objects.get(id=1),
                "payment_amount": 5000.0,
                "payment_methods": 1,
                "payment_status": 1,
            },
        ]

        for payment_data in payments:
            payment, created = Payment.objects.get_or_create(**payment_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Добавление успешно {payment.id}"))
            else:
                self.stdout.write(self.style.WARNING(f"Что-то пошло не так"))
