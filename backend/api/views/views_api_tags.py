from django.contrib.auth.models import *
from django.contrib.auth.validators import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.generics import *
from django.core.exceptions import ObjectDoesNotExist
from registration.views import *
from django.http import JsonResponse
from django.core.cache import cache
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




def redis_test(request):
    try:
        # Записываем данные в кэш
        cache.set('test_key', 'Hello, Redis!', timeout=10000000)
        # Читаем данные из кэша
        value = cache.get('test_key')
        return JsonResponse({'status': 'success', 'message': value})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


class LanguageListView(APIView):
    def get(self, request):
        languages = Language.objects.all()  # Извлекаем все языки
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data)
    

import redis
import pickle
from django.conf import settings
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


class RedisLanguageListView(APIView):
    def get(self, request):
        # Получаем все языки из Redis хеша 'languages'
        language_data = r.hgetall('languages')

        if not language_data:
            return Response({"detail": "No languages found"}, status=status.HTTP_404_NOT_FOUND)

        languages = []
        for lang_id, data in language_data.items():
            try:
                # Десериализуем данные с помощью pickle
                language_data = pickle.loads(data)
                languages.append(language_data)
            except Exception as e:
                print(f"Ошибка при десериализации данных для языка с ID {lang_id}: {e}")

        if not languages:
            return Response({"detail": "Languages not found or invalid data"}, status=status.HTTP_404_NOT_FOUND)

        # Сериализуем и возвращаем результат
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LanguageSearchView(APIView):
    def post(self, request):
        # Получаем параметр 'name' из тела запроса
        language_name = request.data.get('name', None)

        if not language_name:
            return Response({"detail": "Поле 'name' обязательно для поиска языка."}, status=status.HTTP_400_BAD_REQUEST)

        # Формируем ключ для Redis, используя имя языка
        cache_key = f':1:language:{language_name}'

        # Пытаемся найти язык в кэше Redis
        language_data = r.get(cache_key)
        
        if language_data:
            # Если данные найдены в кэше, десериализуем их
            try:
                language = pickle.loads(language_data)
                serializer = LanguageSerializer(language)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"detail": f"Ошибка при десериализации данных: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Если языка нет в кэше, проверяем в базе данных
        try:
            language = Language.objects.get(name=language_name)
            # Сохраняем данные в кэш для дальнейшего использования
            #r.set(cache_key, pickle.dumps(language))
            serializer = LanguageSerializer(language)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"detail": "Язык не найден"}, status=status.HTTP_404_NOT_FOUND)
        


class RedisTagListAPIView(APIView):
    def get(self, request):
        # Получаем все теги из Redis хеша 'tags'
        tag_data = r.hgetall('tags')

        if not tag_data:
            return Response({"detail": "No tags found"}, status=status.HTTP_404_NOT_FOUND)

        tags = []
        for tag_id, data in tag_data.items():
            try:
                # Десериализуем данные с помощью pickle
                tag_data = pickle.loads(data)
                tags.append(tag_data)
            except Exception as e:
                print(f"Ошибка при десериализации данных для тега с ID {tag_id}: {e}")

        if not tags:
            return Response({"detail": "Tags not found or invalid data"}, status=status.HTTP_404_NOT_FOUND)
        
        # Сериализуем и возвращаем результат
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)