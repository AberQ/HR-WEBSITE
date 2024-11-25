# serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

from rest_framework import serializers

from .models import *


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ["id", "email", "password", "first_name", "last_name", "patronymic"]
    
    def create(self, validated_data):
        user = Applicant(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            patronymic=validated_data.get("patronymic", ""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ["id", "email", "password", "company_name", "company_info"]

    def create(self, validated_data):
        user = Employer(
            email=validated_data["email"],
            company_name=validated_data["company_name"],
            company_info=validated_data.get("company_info", ""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавляем роль пользователя в токен
        if hasattr(user, "applicant"):
            token["role"] = "Applicant"
        elif hasattr(user, "employer"):
            token["role"] = "Employer"
        else:
            token["role"] = "Admin"  # Если не подходит под другие роли

        return token
