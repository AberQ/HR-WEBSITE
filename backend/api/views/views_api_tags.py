from rest_framework import generics
from ..models import Vacancy
from ..serializers import *
from rest_framework import generics
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework import status
from ..models import Vacancy
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from registration.views import *
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from registration.forms import VacancyForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..models import Vacancy
from rest_framework import permissions
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from ..models import Vacancy
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .swagger_properties import *
class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagCreateView(CreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @swagger_auto_schema(
        operation_summary="Создать новый тег технологического стека",
        operation_description=(
            "Эндпоинт для создания нового тега технологического стека. "
            "Необходимо отправить данные в формате JSON, указав название тега.Авторизация не нужна"
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Название тега (например, 'Python', 'Django')",
                    example="Django"
                ),
            },
            required=["name"]
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                "Тег успешно создан",
                TagSerializer
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                "Ошибка валидации данных",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Описание ошибки",
                            example="Поле 'name' не может быть пустым."
                        )
                    }
                )
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)