# Generated by Django 5.1.6 on 2025-02-19 11:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0005_course_owner_lesson_owner"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                help_text="Владелец курса",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="course",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                help_text="Владелец лекции",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="lesson",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
