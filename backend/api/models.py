from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class WorkConditionTag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Условие работы')

    class Meta:
        verbose_name = 'Условие работы'
        verbose_name_plural = 'Условия работы'

    def __str__(self):
        return self.name

class TechStackTag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Технология')

    class Meta:
        verbose_name = 'Технология'
        verbose_name_plural = 'Технологии'

    def __str__(self):
        return self.name

class Vacancy(models.Model):
    WORK_FORMAT_CHOICES = [
        ('remote', 'Удаленная'),
        ('hybrid', 'Гибридная'),
        ('onsite', 'Очная'),
    ]

    WORK_CONDITION_CHOICES = [
        ('full_time', 'Полная ставка'),
        ('part_time', 'Неполная ставка'),
        ('internship', 'Стажировка'),
        ('volunteering', 'Волонтерство'),
        ('one_time', 'Разовое задание'),
        ('project', 'Проектная работа'),
    ]
    CURRENCY_CHOICES = [
        ('RUB', 'RUB'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    ]

    EXPERIENCE_CHOICES = [
        ('0', 'Без опыта'),
        ('1', 'До 1 года'),
        ('1-3', 'от 1 до 3 лет'),
        ('3-6', 'от 3 до 6 лет'),
        ('6', 'более 6 лет'),
    ]

    STATUS_CHOICES = [
        ('published', 'Опубликована'),
        ('archived', 'В архиве'),
        ('checking', 'На проверке'),
    ]

    title = models.CharField(max_length=255, verbose_name='Название')
    work_format = models.CharField(
        max_length=10, 
        choices=WORK_FORMAT_CHOICES, 
        default='onsite',
        verbose_name='Формат работы'
    )
    min_salary = models.PositiveIntegerField(verbose_name='Минимальная зарплата')
    max_salary = models.PositiveIntegerField(verbose_name='Максимальная зарплата')
    currency = models.CharField(
        max_length=3, 
        choices=CURRENCY_CHOICES, 
        default='RUB',
        verbose_name='Валюта'
    )
    experience = models.CharField(
        max_length=10, 
        choices=EXPERIENCE_CHOICES, 
        default='0',
        verbose_name='Опыт работы'
    )
    city = models.CharField(max_length=255, verbose_name='Город')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    number_of_openings = models.PositiveIntegerField(verbose_name='Количество вакантных мест')
    description = models.TextField(verbose_name='Описание')
    tech_stack_tags = models.ManyToManyField('TechStackTag', blank=True, verbose_name='Навыки')
    work_condition_tags = models.CharField(
        max_length=20, 
        choices=WORK_CONDITION_CHOICES, 
        default='full_time',
        verbose_name='Условие работы'
    )
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='published',
        verbose_name='Статус'
    )

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def formatted_publication_date(self):
        return self.publication_date.strftime('%d %B %Y, %H:%M')
    
    def clean(self):
        super().clean()
        if self.number_of_openings <= 0:
            raise ValidationError('Количество мест должно быть больше 0.')
        if self.min_salary > self.max_salary:
            raise ValidationError('Минимальная зарплата не может превышать максимальную.')

    def save(self, *args, **kwargs):
        if self.status == 'published':
            self.publication_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
