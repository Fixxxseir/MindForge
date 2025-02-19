# Generated by Django 5.1.6 on 2025-02-19 11:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0004_alter_lesson_course"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                help_text="Владелец курса",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="course",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="lesson",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                help_text="Владелец лекции",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="lesson",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
