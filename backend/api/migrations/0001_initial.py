# Generated by Django 4.2.6 on 2024-10-30 18:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TechStackTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, unique=True, verbose_name="Навык"),
                ),
            ],
            options={
                "verbose_name": "Навык",
                "verbose_name_plural": "Навыки",
            },
        ),
        migrations.CreateModel(
            name="WorkConditionTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Условие работы"
                    ),
                ),
            ],
            options={
                "verbose_name": "Условие работы",
                "verbose_name_plural": "Условия работы",
            },
        ),
        migrations.CreateModel(
            name="Vacancy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Название")),
                (
                    "work_format",
                    models.CharField(
                        choices=[
                            ("remote", "Удаленная"),
                            ("hybrid", "Гибридная"),
                            ("onsite", "Очная"),
                        ],
                        default="onsite",
                        max_length=10,
                        verbose_name="Формат работы",
                    ),
                ),
                (
                    "min_salary",
                    models.PositiveIntegerField(verbose_name="Минимальная зарплата"),
                ),
                (
                    "max_salary",
                    models.PositiveIntegerField(verbose_name="Максимальная зарплата"),
                ),
                (
                    "currency",
                    models.CharField(
                        choices=[("RUB", "RUB"), ("USD", "USD"), ("EUR", "EUR")],
                        default="RUB",
                        max_length=3,
                        verbose_name="Валюта",
                    ),
                ),
                (
                    "experience",
                    models.CharField(
                        choices=[
                            ("0", "Без опыта"),
                            ("1", "До 1 года"),
                            ("1-3", "от 1 до 3 лет"),
                            ("3-6", "от 3 до 6 лет"),
                            ("6", "более 6 лет"),
                        ],
                        default="0",
                        max_length=10,
                        verbose_name="Опыт работы",
                    ),
                ),
                ("city", models.CharField(max_length=255, verbose_name="Город")),
                ("address", models.CharField(max_length=255, verbose_name="Адрес")),
                (
                    "number_of_openings",
                    models.PositiveIntegerField(
                        verbose_name="Количество вакантных мест"
                    ),
                ),
                ("description", models.TextField(verbose_name="Описание")),
                (
                    "work_condition_tags",
                    models.CharField(
                        choices=[
                            ("full_time", "Полная ставка"),
                            ("part_time", "Неполная ставка"),
                            ("internship", "Стажировка"),
                            ("volunteering", "Волонтерство"),
                            ("one_time", "Разовое задание"),
                            ("project", "Проектная работа"),
                        ],
                        default="full_time",
                        max_length=20,
                        verbose_name="Условие работы",
                    ),
                ),
                (
                    "publication_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата публикации"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("published", "Опубликована"),
                            ("archived", "В архиве"),
                            ("checking", "На проверке"),
                        ],
                        default="published",
                        max_length=10,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Создатель вакансии",
                    ),
                ),
                (
                    "tech_stack_tags",
                    models.ManyToManyField(
                        blank=True, to="api.techstacktag", verbose_name="Навыки"
                    ),
                ),
            ],
            options={
                "verbose_name": "Вакансия",
                "verbose_name_plural": "Вакансии",
            },
        ),
    ]
