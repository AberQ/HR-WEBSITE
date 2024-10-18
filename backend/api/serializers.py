from rest_framework import serializers
from .models import *

class VacancySerializer(serializers.ModelSerializer):
    work_format = serializers.ChoiceField(choices=Vacancy.WORK_FORMAT_CHOICES, required=True)
    work_condition_tags = serializers.ChoiceField(choices=Vacancy.WORK_CONDITION_CHOICES, required=True)

    class Meta:
        model = Vacancy
        fields = '__all__'