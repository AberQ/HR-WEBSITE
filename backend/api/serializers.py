from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Vacancy, Tag, WorkConditionTag
User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']  
    

class SkillsSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(), 
        many=True, 
        slug_field='name'
    )
    languages = serializers.SlugRelatedField(
        many=True, queryset=Language.objects.all(), slug_field='name'
    )
    class Meta:
        model = Vacancy
        fields = ['experience', 'tags', 'languages']

    def get_tags(self, obj):
        # Получаем все теги и возвращаем их названия
        return [tag.name for tag in obj.tags.all()]
class WorkConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy 
        fields = ['format', 'employment_type']

class LocationSerializerForVacancy(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ['city', 'address']

class LocationSerializerForResume(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['city']

class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ['min_salary', 'max_salary', 'currency']

class ResumeContacts(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['email', "phone"]
class VacancySerializer(serializers.ModelSerializer):
    skills = SkillsSerializer(source='*')
    work_conditions = WorkConditionsSerializer(source='*')
    location = LocationSerializerForVacancy(source='*')
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
    location = LocationSerializerForResume(source="*")
    contacts = ResumeContacts(source="*")
    class Meta:
        model = Resume
        fields = [
            'id',
            'desired_position',
            'candidate_name',
            'content',
            'contacts',
            'location',
            'degree',
            'skills',           
            'portfolio_link',
            'updated_at',
            'applicant',
        ]

    def get_tags(self, obj):
        return [skill.name for skill in obj.tags.all()]

    def get_languages(self, obj):
        return [language.name for language in obj.languages.all()]
    


class ResumeSerializerForCreateAPI(serializers.ModelSerializer):
    skills = SkillsSerializer(source='*')
    location = LocationSerializerForResume(source="*")
    contacts = ResumeContacts(source="*")
    class Meta:
        model = Resume
        fields = [
            'id',
            'desired_position',
            'candidate_name',
            'content',
            'contacts',
            'location',
            'degree',
            'skills',    
            'portfolio_link',
            'updated_at',
        ]

    def get_tags(self, obj):
        # Возвращаем список тегов навыков для этого резюме
        return [tech_stack.name for tech_stack in obj.tags.all()]

    def get_languages(self, obj):
        # Возвращаем список языков для этого резюме
        return [language.name for language in obj.languages.all()]

    def create(self, validated_data):
        # Извлекаем списки для languages и tags
        tags = validated_data.pop('tags', [])
        languages = validated_data.pop('languages', [])
        resume = Resume.objects.create(**validated_data)

        # Устанавливаем многие ко многим (если необходимо)
        resume.tags.set(tags)
        resume.languages.set(languages)
        resume.save()

        return resume



class VacancySerializerForCreateAPI(serializers.ModelSerializer):
    skills = SkillsSerializer(source='*')
    work_conditions = WorkConditionsSerializer(source='*')
    location = LocationSerializerForVacancy(source='*')
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
        tags = validated_data.pop('tags', [])
        employment_type = validated_data.pop('employment_type', [])
        languages = validated_data.pop('languages', [])
        vacancy = Vacancy.objects.create(**validated_data)

        # Устанавливаем многие ко многим (если необходимо)
        vacancy.tags.set(tags)
        vacancy.employment_type = employment_type  # Установите правильное поле для условий работы
        vacancy.languages.set(languages)
        vacancy.save()

        return vacancy

    def update(self, instance, validated_data):
        # Валидация и обновление существующей вакансии
        tags = validated_data.pop('tags', None)
        employment_type = validated_data.pop('employment_type', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if tags is not None:
            instance.tags.set(tags)

        if employment_type is not None:
            instance.employment_type = employment_type

        instance.save()
        return instance