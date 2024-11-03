from rest_framework import serializers
from .models import Vacancy, TechStackTag, WorkConditionTag
from django.contrib.auth import get_user_model

User = get_user_model()

# serializers.py
class VacancySerializer(serializers.ModelSerializer):
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
            'created_by',          # Создатель вакансии
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