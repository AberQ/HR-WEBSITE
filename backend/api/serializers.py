from rest_framework import serializers
from .models import Vacancy, TechStackTag, WorkConditionTag
from django.contrib.auth import get_user_model

User = get_user_model()

# serializers.py
class VacancySerializer(serializers.ModelSerializer):
    work_format = serializers.ChoiceField(choices=Vacancy.WORK_FORMAT_CHOICES, required=True)
    currency = serializers.ChoiceField(choices=Vacancy.CURRENCY_CHOICES, required=True)
    experience = serializers.ChoiceField(choices=Vacancy.EXPERIENCE_CHOICES, required=True)
    status = serializers.ChoiceField(choices=Vacancy.STATUS_CHOICES, required=True)
    
    work_condition_tags = serializers.ChoiceField(choices=Vacancy.WORK_CONDITION_CHOICES, required=True)
    
    tech_stack_tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=TechStackTag.objects.all(),
        required=False
    )
    
    created_by = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all(),
        required=True
    )

    class Meta:
        model = Vacancy
        # Укажите порядок полей в том порядке, в котором хотите видеть их в JSON
        fields = [
            'id','title', 'city', 'address', 'work_format', 'experience', 'min_salary', 
            'max_salary', 'currency', 'number_of_openings', 'description', 'tech_stack_tags',
            'work_condition_tags', 'status', 'publication_date', 'created_by'
        ]
