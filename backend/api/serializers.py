from rest_framework import serializers
from .models import *

class VacancySerializer(serializers.ModelSerializer):
    work_format = serializers.ChoiceField(choices=Vacancy.WORK_FORMAT_CHOICES, required=True)
    
    # Меняем на MultipleChoiceField для ManyToManyField work_condition_tags
    work_condition_tags = serializers.ChoiceField(choices=Vacancy.WORK_CONDITION_CHOICES, required=True)
    
    # Используем SlugRelatedField для tech_stack_tags, чтобы отображать названия
    tech_stack_tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',  # Отображаем имена тегов вместо ID
        queryset=TechStackTag.objects.all(),
        required=False  # Поле необязательное
    )

    class Meta:
        model = Vacancy
        fields = '__all__'