from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

# serializers.py
class VacancySerializerForCreateAPI(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = [
            'id',                  # Поле ID, если нужно
            'title',               # Название вакансии
            'description',         # Описание вакансии
            'work_format',         # Формат работы
            'min_salary',          # Минимальная зарплата
            'max_salary',          # Максимальная зарплата
            'currency',            # Валюта
            'experience',          # Опыт работы
            'city',                # Город
            'address',             # Адрес
            'number_of_openings',  # Количество вакантных мест
            'tech_stack_tags',     # Навыки (многие ко многим)
            'work_condition_tags',  # Условия работы
            'publication_date',    # Дата публикации
            'status',              # Статус
            
        ]

    def create(self, validated_data):
        # Валидация и создание новой вакансии
        tech_stack_tags = validated_data.pop('tech_stack_tags', [])
        work_condition_tags = validated_data.pop('work_condition_tags', [])

        vacancy = Vacancy.objects.create(**validated_data)

        # Устанавливаем многие ко многим (если необходимо)
        vacancy.tech_stack_tags.set(tech_stack_tags)
        vacancy.work_condition_tags = work_condition_tags  # Установите правильное поле для условий работы
        vacancy.save()

        return vacancy

    def update(self, instance, validated_data):
        # Валидация и обновление существующей вакансии
        tech_stack_tags = validated_data.pop('tech_stack_tags', None)
        work_condition_tags = validated_data.pop('work_condition_tags', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if tech_stack_tags is not None:
            instance.tech_stack_tags.set(tech_stack_tags)

        if work_condition_tags is not None:
            instance.work_condition_tags = work_condition_tags

        instance.save()
        return instance
    
from rest_framework import serializers
from .models import Vacancy, TechStackTag, WorkConditionTag
class SkillsSerializer(serializers.ModelSerializer):
    # Добавляем метод для получения названий тегов
    tech_stack_tags = serializers.SerializerMethodField()

    class Meta:
        model = Vacancy
        fields = ['experience', 'tech_stack_tags']

    def get_tech_stack_tags(self, obj):
        # Получаем все теги и возвращаем их названия
        return [tag.name for tag in obj.tech_stack_tags.all()]
class WorkConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ['work_format', 'work_condition_tags']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ['city', 'address']

class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ['min_salary', 'max_salary', 'currency']

class VacancySerializer(serializers.ModelSerializer):
    skills = SkillsSerializer(source='*')
    work_condition = WorkConditionSerializer(source='*')
    location = LocationSerializer(source='*')
    salary = SalarySerializer(source='*')

    class Meta:
        model = Vacancy
        fields = [
            'id',
            'title',
            'description',
            'work_condition',
            'salary',
            'location',
            'number_of_openings',
            'skills',
            'publication_date',
            'status',
            'created_by',
        ]
        read_only_fields = ['created_by']  # Делает поле created_by доступным только для чтения

    def update(self, instance, validated_data):
        # Убираем 'created_by' из validated_data, если оно присутствует
        validated_data.pop('created_by', None)  # Исключаем created_by из данных, чтобы не было ошибки

        # Сохраняем обновленный объект
        return super().update(instance, validated_data)


class ResumeSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = '__all__'

    def get_skills(self, obj):
        return [skill.name for skill in obj.skills.all()]

    def get_languages(self, obj):
        return [language.name for language in obj.languages.all()]