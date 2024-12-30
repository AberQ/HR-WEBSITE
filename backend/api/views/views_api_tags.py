from django.contrib.auth.models import *
from django.contrib.auth.validators import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.generics import *

from registration.views import *

from ..serializers import *
from .swagger_properties import *


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @swagger_auto_schema(
        operation_summary="Получить список тегов",
        operation_description="Возвращает список всех доступных тегов.",
        responses={
            200: openapi.Response(
                description="Успешный запрос",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "name": "Programming",
                            
                        },
                        {
                            "id": 2,
                            "name": "Design",
                            
                        }
                    ]
                },
                schema=TagSerializer(many=True)
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
class TagDetailAPIView(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'id'


    @swagger_auto_schema(
        operation_summary="Получить тег по ID",
        operation_description="Возвращает данные тега с указанным ID.",
        responses={
            200: openapi.Response(
                description="Успешный запрос",
                examples={
                    "application/json": {
                        "id": 1,
                        "name": "JavaScript"
                    }
                },
                schema=TagSerializer
            ),
            404: openapi.Response(
                description="Тег не найден",
                examples={
                    "application/json": {
                        "detail": "No Tag matches the given query."
                    }
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class TagCreateView(CreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @swagger_auto_schema(
    operation_summary="Создать новый тег технологического стека",
    operation_description=(
        "Эндпоинт для создания нового тега технологического стека. "
        "Необходимо отправить данные в формате JSON, указав название тега. Авторизация не нужна."
    ),
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Название тега (например, 'Python', 'Django')",
                example="Django",
            ),
        },
        required=["name"],
        example={
            "name": "Django"
        },
    ),
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            "Тег успешно создан",
            schema=TagSerializer,
            examples={
                "application/json": {
                    "id": 1,
                    "name": "Django"
                }
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            "Ошибка валидации данных",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Описание ошибки",
                        example="Поле 'name' не может быть пустым.",
                    )
                },
            ),
            examples={
                "application/json": {
                    "error": "Поле 'name' не может быть пустым."
                }
            }
        ),
    },
)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


from django.http import JsonResponse
from django.core.cache import cache

def redis_test(request):
    try:
        # Записываем данные в кэш
        cache.set('test_key', 'Hello, Redis!', timeout=10000000)
        # Читаем данные из кэша
        value = cache.get('test_key')
        return JsonResponse({'status': 'success', 'message': value})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
