from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class TechStackTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechStackTag
        fields = ['id', 'name']  
    
from rest_framework import serializers
from .models import Vacancy, TechStackTag, WorkConditionTag
class SkillsSerializer(serializers.ModelSerializer):
    tech_stack_tags = serializers.SlugRelatedField(
        queryset=TechStackTag.objects.all(), 
        many=True, 
        slug_field='name'
    )

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
            'applicant',

        ]

    def get_tech_stack_tags(self, obj):
        return [skill.name for skill in obj.tech_stack_tags.all()]

    def get_languages(self, obj):
        return [language.name for language in obj.languages.all()]
    


class ResumeSerializerForCreateAPI(serializers.ModelSerializer):
    tech_stack_tags = serializers.ListField(child=serializers.CharField(), write_only=True)
    languages = serializers.ListField(child=serializers.CharField(), write_only=True)

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

    def create(self, validated_data):
        # Извлекаем списки для languages и tech_stack_tags
        languages_data = validated_data.pop('languages', [])
        tech_stack_tags_data = validated_data.pop('tech_stack_tags', [])

        # Создаем экземпляр резюме
        resume = Resume.objects.create(**validated_data)

        # Создаем и связываем языки с резюме
        for language_name in languages_data:
            language, created = Language.objects.get_or_create(name=language_name)
            resume.languages.add(language)

        # Создаем и связываем теги навыков с резюме
        for tech_stack_tag_name in tech_stack_tags_data:
            tech_stack_tag, created = TechStackTag.objects.get_or_create(name=tech_stack_tag_name)
            resume.tech_stack_tags.add(tech_stack_tag)

        return resume

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