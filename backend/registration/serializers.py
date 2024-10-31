# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

from rest_framework import serializers
from .models import Applicant

class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ['email', 'password', 'first_name', 'last_name', 'patronymic']

    def create(self, validated_data):
        user = Applicant(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            patronymic=validated_data.get('patronymic', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user