from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Vacancy, TechStackTag, WorkConditionTag
User = get_user_model()


class TechStackTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechStackTag
        fields = ['id', 'name']  
    

class SkillsSerializer(serializers.ModelSerializer):
    tech_stack_tags = serializers.SlugRelatedField(
        queryset=TechStackTag.objects.all(), 
        many=True, 
        slug_field='name'
    )
    languages = serializers.SlugRelatedField(
        many=True, queryset=Language.objects.all(), slug_field='name'
    )
    class Meta:
        model = Vacancy
        fields = ['experience', 'tech_stack_tags', 'languages']

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
    skills = SkillsSerializer(source='*')
    applicant = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Resume
        fields = [
            'id',
            'desired_position',
            'candidate_name',
            'email',
            'phone',
            'content',
            'city',
            'degree',
            'skills',           
            'portfolio_link',
            'updated_at',
            'applicant',
        ]

    def get_tech_stack_tags(self, obj):
        return [skill.name for skill in obj.tech_stack_tags.all()]

    def get_languages(self, obj):
        return [language.name for language in obj.languages.all()]
    


class ResumeSerializerForCreateAPI(serializers.ModelSerializer):
    skills = SkillsSerializer(source='*')

    class Meta:
        model = Resume
        fields = [
            'id',
            'desired_position',
            'candidate_name',
            'email',
            'phone',
            'content',
            'city',
            'degree',
            'skills',    
            'portfolio_link',
            'updated_at',
        ]

    def get_tech_stack_tags(self, obj):
        # Возвращаем список тегов навыков для этого резюме
        return [tech_stack.name for tech_stack in obj.tech_stack_tags.all()]

    def get_languages(self, obj):
        # Возвращаем список языков для этого резюме
        return [language.name for language in obj.languages.all()]

    def create(self, validated_data):
        # Извлекаем списки для languages и tech_stack_tags
        tech_stack_tags = validated_data.pop('tech_stack_tags', [])
        languages = validated_data.pop('languages', [])
        resume = Resume.objects.create(**validated_data)

        # Устанавливаем многие ко многим (если необходимо)
        resume.tech_stack_tags.set(tech_stack_tags)
        resume.languages.set(languages)
        resume.save()

        return resume



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
        languages = validated_data.pop('languages', [])
        vacancy = Vacancy.objects.create(**validated_data)

        # Устанавливаем многие ко многим (если необходимо)
        vacancy.tech_stack_tags.set(tech_stack_tags)
        vacancy.employment_type = employment_type  # Установите правильное поле для условий работы
        vacancy.languages.set(languages)
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