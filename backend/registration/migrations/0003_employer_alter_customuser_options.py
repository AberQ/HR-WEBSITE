# Generated by Django 4.2.6 on 2024-10-31 14:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("registration", "0002_remove_customuser_first_name_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Employer",
            fields=[
                (
                    "customuser_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=150, verbose_name="first name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=150, verbose_name="last name"),
                ),
                (
                    "patronymic",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="Отчество"
                    ),
                ),
            ],
            options={
                "verbose_name": "Соискатель",
                "verbose_name_plural": "Соискатели",
            },
            bases=("registration.customuser",),
        ),
        migrations.AlterModelOptions(
            name="customuser",
            options={
                "verbose_name": "Авторизационник",
                "verbose_name_plural": "Авторизационники",
            },
        ),
    ]
