from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

# serializers.py

    
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
class WorkConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy 
        fields = ['format', 'employment_type']

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
    work_conditions = WorkConditionsSerializer(source='*')
    location = LocationSerializer(source='*')
    salary = SalarySerializer(source='*')

    class Meta:
        model = Vacancy
        fields = [
            'id',
            'title',
            'description',
            'work_conditions',
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
    tech_stack_tags = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = [
            'id',
            'desired_position',
            'candidate_name',
            'email',
            'phone',
            'city',
            'degree',
            'work_experience',
            'languages',         
            'tech_stack_tags',            
            'portfolio_link',
            'updated_at',

        ]

    def get_tech_stack_tags(self, obj):
        return [skill.name for skill in obj.tech_stack_tags.all()]

    def get_languages(self, obj):
        return [language.name for language in obj.languages.all()]


class VacancySerializerForCreateAPI(serializers.ModelSerializer):
    skills = SkillsSerializer(source='*')
    work_conditions = WorkConditionsSerializer(source='*')
    location = LocationSerializer(source='*')
    salary = SalarySerializer(source='*')

    class Meta:
        model = Vacancy
        fields = [
            'id',
            'title',
            'description',
            'work_conditions',
            'salary',
            'location',
            'number_of_openings',
            'skills',
            'publication_date',
            'status',
        ]

    def create(self, validated_data):
        # Валидация и создание новой вакансии
        tech_stack_tags = validated_data.pop('tech_stack_tags', [])
        employment_type = validated_data.pop('employment_type', [])

        vacancy = Vacancy.objects.create(**validated_data)

        # Устанавливаем многие ко многим (если необходимо)
        vacancy.tech_stack_tags.set(tech_stack_tags)
        vacancy.employment_type = employment_type  # Установите правильное поле для условий работы
        vacancy.save()

        return vacancy

    def update(self, instance, validated_data):
        # Валидация и обновление существующей вакансии
        tech_stack_tags = validated_data.pop('tech_stack_tags', None)
        employment_type = validated_data.pop('employment_type', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if tech_stack_tags is not None:
            instance.tech_stack_tags.set(tech_stack_tags)

        if employment_type is not None:
            instance.employment_type = employment_type

        instance.save()
        return instance