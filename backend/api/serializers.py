from rest_framework import serializers
from .models import Vacancy, TechStackTag  # Убедитесь, что вы импортировали ваши модели
from django.contrib.auth import get_user_model

User = get_user_model()

class VacancySerializer(serializers.ModelSerializer):
    work_format = serializers.ChoiceField(choices=Vacancy.WORK_FORMAT_CHOICES, required=True)
    
    # Изменено на MultipleChoiceField для поддержки множественного выбора
    work_condition_tags = serializers.MultipleChoiceField(choices=Vacancy.WORK_CONDITION_CHOICES, required=True)
    
    # Используем SlugRelatedField для tech_stack_tags, чтобы отображать названия
    tech_stack_tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',  # Отображаем имена тегов вместо ID
        queryset=TechStackTag.objects.all(),
        required=False  # Поле необязательное
    )
    
    # Добавляем поле для отображения создателя вакансии
    created_by = serializers.SlugRelatedField(
        slug_field='email',  # Отображаем email пользователя
        queryset=User.objects.all(),
        required=True
    )

    class Meta:
        model = Vacancy
        fields = '__all__'
