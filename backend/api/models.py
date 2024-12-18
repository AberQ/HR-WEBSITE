from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.core.cache import cache
from registration.models import *

EXPERIENCE_CHOICES = [
    ("0", "Без опыта"),
    ("1", "До 1 года"),
    ("1-3", "от 1 до 3 лет"),
    ("3-6", "от 3 до 6 лет"),
    ("6", "более 6 лет"),
]


class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name="Язык")

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        # Сохраняем в Redis при сохранении
        cache.set(f'language:{self.id}', self, timeout=None)
        super().save(*args, **kwargs)

    @staticmethod
    def get_by_id(language_id):
        # Проверяем, есть ли язык в кеше
        language = cache.get(f'language:{language_id}')
        if not language:
            # Если языка нет в кеше, извлекаем из базы данных и сохраняем в кеш
            language = Language.objects.get(id=language_id)
            cache.set(f'language:{language_id}', language, timeout=None)
        return language
    
    def delete(self, *args, **kwargs):
        # Удаляем тег из кеша
        cache.delete(f'tag:{self.id}')
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Сохраняем в Redis при сохранении
        cache.set(f'tag:{self.id}', self, timeout=None)  # Время жизни не ограничено
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Удаляем тег из кеша
        cache.delete(f'tag:{self.id}')
        super().delete(*args, **kwargs)

    @staticmethod
    def get_by_id(tag_id):
        # Проверяем, есть ли тег в кеши
        tag = cache.get(f'tag:{tag_id}')
        if not tag:
            # Если тега нет в кеше, извлекаем из базы данных и сохраняем в кеш
            tag = Tag.objects.get(id=tag_id)
            cache.set(f'tag:{tag_id}', tag, timeout=None)
        return tag

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"


class Vacancy(models.Model):
    WORK_FORMAT_CHOICES = [
        ("remote", "Удаленная"),
        ("hybrid", "Гибридная"),
        ("onsite", "Очная"),
    ]

    WORK_CONDITION_CHOICES = [
        ("full_time", "Полная ставка"),
        ("part_time", "Неполная ставка"),
        ("internship", "Стажировка"),
        ("volunteering", "Волонтерство"),
        ("one_time", "Разовое задание"),
        ("project", "Проектная работа"),
    ]

    CURRENCY_CHOICES = [
        ("RUB", "RUB"),
        ("USD", "USD"),
        ("EUR", "EUR"),
    ]

    STATUS_CHOICES = [
        ("published", "Опубликована"),
        ("archived", "В архиве"),
        ("checking", "На проверке"),
    ]

    title = models.CharField(max_length=255, verbose_name="Название")
    format = models.CharField(
        max_length=10,
        choices=WORK_FORMAT_CHOICES,
        default="onsite",
        verbose_name="Формат работы",
    )
    min_salary = models.PositiveIntegerField(verbose_name="Минимальная зарплата")
    max_salary = models.PositiveIntegerField(verbose_name="Максимальная зарплата")
    currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, default="RUB", verbose_name="Валюта"
    )
    experience = models.CharField(
        max_length=10,
        choices=EXPERIENCE_CHOICES,
        default="0",
        verbose_name="Опыт работы",
    )
    city = models.CharField(max_length=255, verbose_name="Город")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    number_of_openings = models.PositiveIntegerField(
        verbose_name="Количество вакантных мест"
    )
    description = models.TextField(verbose_name="Описание")
    tags = models.ManyToManyField("Tag", blank=True, verbose_name="Навыки")
    languages = models.ManyToManyField(Language, blank=True, verbose_name="Языки")
    employment_type = models.CharField(
        max_length=20,
        choices=WORK_CONDITION_CHOICES,
        default="full_time",
        verbose_name="Условие работы",
    )
    publication_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="published",
        verbose_name="Статус",
    )
    created_by = models.ForeignKey(
        Employer,  # Указываем модель работодателя
        on_delete=models.CASCADE,
        verbose_name="Создатель вакансии",
    )

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def formatted_publication_date(self):
        return self.publication_date.strftime("%d %B %Y, %H:%M")

    def clean(self):
        super().clean()
        if self.number_of_openings <= 0:
            raise ValidationError("Количество мест должно быть больше 0.")
        if self.min_salary > self.max_salary:
            raise ValidationError(
                "Минимальная зарплата не может превышать максимальную."
            )

    def save(self, *args, **kwargs):
        if self.status == "published":
            self.publication_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.created_by.company_name}"  # Отображаем название вакансии и название компании


class Resume(models.Model):
    # Валидатор для work_experience, чтобы вводились только цифры
    def validate_numeric_experience(value):
        if not value.isdigit():
            raise ValidationError(("Опыт работы должен содержать только цифры."))

    DEGREE_CHOICES = [
        ("speciality", "Специалитет"),
        ("bachelor", "Бакалавриат"),
        ("unfinished_higher", "Неоконченное высшее"),
        ("vocational", "СПО"),
        ("unfinished_secondary", "Неоконченное среднее"),
    ]

    # Основная информация
    desired_position = models.CharField(
        max_length=255, verbose_name="Желаемая должность"
    )
    candidate_name = models.CharField(max_length=255, verbose_name="Имя кандидата")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    city = models.CharField(max_length=255, verbose_name="Город")
    content = models.CharField(max_length=255, verbose_name="Описание резюме")
    # Специальность
    specialization = models.CharField(
        max_length=255, verbose_name="Специальность"
    )  # Новое поле перед степенью

    # Образование
    degree = models.CharField(
        max_length=100, choices=DEGREE_CHOICES, verbose_name="Степень"
    )

    # Опыт работы
    experience = models.CharField(
        max_length=10,
        choices=EXPERIENCE_CHOICES,
        default="0",
        verbose_name="Опыт работы",
    )

    # Навыки
    tags = models.ManyToManyField(
        "Tag", blank=True, verbose_name="Навыки"
    )  # Связь с Tag

    # Дополнительные разделы
    languages = models.ManyToManyField(Language, blank=True, verbose_name="Языки")
    portfolio_link = models.URLField(blank=True, verbose_name="Ссылка на портфолио")

    # Временные метки
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    applicant = models.ForeignKey(
        Applicant, on_delete=models.CASCADE, related_name="applicant_resumes"
    )

    class Meta:
        verbose_name = "Резюме"
        verbose_name_plural = "Резюме"

    def __str__(self):
        return f"{self.candidate_name} - {self.desired_position}"
