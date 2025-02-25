from django.db import models

from config import settings


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название курса", help_text="Введите название курса")
    image_preview = models.ImageField(
        upload_to="courses/preview",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите изображение для превью курса",
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание курса", help_text="Введите описание курса"
    )
    time_create = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    time_update = models.DateTimeField(auto_now=True, blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="course",
        help_text="Владелец курса",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, null=True, blank=True, related_name="lessons", verbose_name="Курс"
    )
    title = models.CharField(max_length=255, verbose_name="Название урока", help_text="Введите название урока")
    description = models.TextField(blank=True, null=True, verbose_name="Описание урока")
    image_preview = models.ImageField(
        upload_to="lessons/preview",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите изображение для превью урока",
    )
    video_link = models.URLField(verbose_name="Ссылка на видео", null=True, blank=True)
    time_create = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    time_update = models.DateTimeField(auto_now=True, blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="lesson",
        help_text="Владелец лекции",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
