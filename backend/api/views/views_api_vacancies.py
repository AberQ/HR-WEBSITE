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


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#API для вакансий
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class VacancyListAPIView(generics.ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    #permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Получить список всех вакансий на сайте",
        operation_description="Получить список всех вакансий. Авторизация не требуется",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Список всех вакансий",
                examples={
                    'application/json': [
    {
        "id": 1,
        "title": "Junior Python Developer",
        "description": "Описание вакансии для теста.",
        "work_conditions": {
            "format": "onsite",
            "employment_type": "full_time"
        },
        "salary": {
            "min_salary": 50000,
            "max_salary": 70000,
            "currency": "RUB"
        },
        "location": {
            "city": "Москва",
            "address": "Улица фронтендеров, 69"
        },
        "number_of_openings": 1,
        "skills": {
            "experience": "До 1 года",
            "tags": [
                "Python",
                "Дружелюбность"
            ],
            "languages": [
                "Русский",
                "Английский"
            ]
        },
        "publication_date": "2024-11-19T21:06:28.901506+03:00",
        "status": "Published",
        "created_by": 2
    },
    {
        "id": 2,
        "title": "Junior Python Developer",
        "description": "Описание вакансии для теста.",
        "work_conditions": {
            "format": "onsite",
            "employment_type": "full_time"
        },
        "salary": {
            "min_salary": 50000,
            "max_salary": 70000,
            "currency": "RUB"
        },
        "location": {
            "city": "Москва",
            "address": "Улица фронтендеров, 69"
        },
        "number_of_openings": 1,
        "skills": {
            "experience": "0",
            "tags": [
                "Python",
                "Дружелюбность"
            ],
            "languages": [
                "Русский",
                "Английский"
            ]
        },
        "publication_date": "2024-11-19T22:36:10.027244+03:00",
        "status": "published",
        "created_by": 2
    }
]
                }
            ),
            status.HTTP_400_BAD_REQUEST: 'Неверный запрос. Пожалуйста, проверьте параметры.',
        },
        parameters=[
            openapi.Parameter(
                'search', openapi.IN_QUERY, description="Поиск по заголовку вакансии", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'city', openapi.IN_QUERY, description="Фильтрация по городу", type=openapi.TYPE_STRING
            )
        ]
    )



    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    


    
class VacancyDetailAPIView(generics.RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    lookup_field = 'id'  # Используем 'id' для поиска вакансии по ID
    @swagger_auto_schema(
        operation_summary="Получить детальную информацию о вакансии",
        operation_description="Получить детальную информацию о вакансии по ID. Авторизация не требуется",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Детальная информация о вакансии",
                examples={
                    'application/json': {
    "id": 1,
    "title": "Junior Python Developer",
    "description": "Описание вакансии для теста.",
    "work_conditions": {
        "format": "onsite",
        "employment_type": "full_time"
    },
    "salary": {
        "min_salary": 50000,
        "max_salary": 70000,
        "currency": "RUB"
    },
    "location": {
        "city": "Москва",
        "address": "Улица фронтендеров, 69"
    },
    "number_of_openings": 1,
    "skills": {
        "experience": "До 1 года",
        "tags": [
            "Python",
            "Дружелюбность"
        ],
        "languages": [
            "Русский",
            "Английский"
        ]
    },
    "publication_date": "2024-11-19T21:06:28.901506+03:00",
    "status": "Published",
    "created_by": 2
}
                }
            ),
            status.HTTP_404_NOT_FOUND: 'Вакансия с таким ID не найдена.',
        },
        parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, description="ID вакансии", type=openapi.TYPE_INTEGER
            )
        ]
    )


    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



class VacancyListByEmployerAPIView(generics.ListAPIView):
    serializer_class = VacancySerializer

    def get_queryset(self):
        employer_id = self.kwargs['employer_id']
        return Vacancy.objects.filter(created_by__id=employer_id)

    @swagger_auto_schema(
        operation_summary="Получить список вакансий работодателя",
        operation_description="Получить список вакансий для конкретного работодателя по его ID. Авторизация не требуется",
        responses={
            200: openapi.Response(
                description="Список вакансий работодателя",
                examples={
                    "application/json": [
    {
        "id": 1,
        "title": "Junior Python Developer",
        "description": "Описание вакансии для теста.",
        "work_conditions": {
            "format": "onsite",
            "employment_type": "full_time"
        },
        "salary": {
            "min_salary": 50000,
            "max_salary": 70000,
            "currency": "RUB"
        },
        "location": {
            "city": "Москва",
            "address": "Улица фронтендеров, 69"
        },
        "number_of_openings": 1,
        "skills": {
            "experience": "До 1 года",
            "tags": [
                "Python",
                "Дружелюбность"
            ],
            "languages": [
                "Русский",
                "Английский"
            ]
        },
        "publication_date": "2024-11-19T21:06:28.901506+03:00",
        "status": "Published",
        "created_by": 2
    },
    {
        "id": 2,
        "title": "Junior Python Developer",
        "description": "Описание вакансии для теста.",
        "work_conditions": {
            "format": "onsite",
            "employment_type": "full_time"
        },
        "salary": {
            "min_salary": 50000,
            "max_salary": 70000,
            "currency": "RUB"
        },
        "location": {
            "city": "Москва",
            "address": "Улица фронтендеров, 69"
        },
        "number_of_openings": 1,
        "skills": {
            "experience": "0",
            "tags": [
                "Python",
                "Дружелюбность"
            ],
            "languages": [
                "Русский",
                "Английский"
            ]
        },
        "publication_date": "2024-11-19T22:36:10.027244+03:00",
        "status": "published",
        "created_by": 2
    }
]
                }
            ),
            404: openapi.Response(
                description="Работодатель не найден.",
                examples={
                    "application/json": {"error": "Работодатель не найден."}
                }
            )
        },
        manual_parameters=[
            openapi.Parameter(
                'employer_id',
                openapi.IN_PATH,
                description="ID работодателя",
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        employer_id = self.kwargs['employer_id']
        
        # Проверяем, существует ли работодатель с данным id
        if not Employer.objects.filter(id=employer_id).exists():
            return Response({'error': 'Работодатель не найден.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Если работодатель найден, возвращаем вакансии
        vacancies = self.get_queryset()
        serializer = self.get_serializer(vacancies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class VacancyCreateAPIView(generics.CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializerForCreateAPI
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Создать вакансию",
        operation_description="Создание новой вакансии. Требуется авторизация работодателем. Автор вакансии определяется автоматически по JWT-токену",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["title", "description", "work_conditions", "salary", "location", "number_of_openings", "skills", "status"],
            properties=properties_for_vacancies
    ),
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Вакансия успешно создана.",
                examples={
                    "application/json": {
    "id": 2,
    "title": "Junior Python Developer",
    "description": "Описание вакансии для теста.",
    "work_conditions": {
        "format": "onsite",
        "employment_type": "full_time"
    },
    "salary": {
        "min_salary": 50000,
        "max_salary": 70000,
        "currency": "RUB"
    },
    "location": {
        "city": "Москва",
        "address": "Улица фронтендеров, 69"
    },
    "number_of_openings": 1,
    "skills": {
        "experience": "0",
        "tags": [
            "Python",
            "Дружелюбность"
        ],
        "languages": [
            "Русский",
            "Английский"
        ]
    },
    "publication_date": "2024-11-19T22:36:10.027244+03:00",
    "status": "published"
}
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Некорректные данные для создания вакансии.",
                examples={
                    "application/json": {
                        "error": "Некорректные данные для создания вакансии."
                    }
                }
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Неавторизованный доступ.",
                examples={
                    "application/json": {
                        "detail": "Учетные данные не были предоставлены."
                    }
                }
            ),
            status.HTTP_403_FORBIDDEN: openapi.Response(
                description="Доступ запрещен (не являетесь работодателем).",
                examples={
                    "application/json": {
                        "detail": "Вы не являетесь работодателем и не можете создавать вакансии."
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Проверка на роль пользователя
        if not hasattr(self.request.user, 'employer'):
            raise PermissionDenied("Вы не являетесь работодателем и не можете создавать вакансии.")
        
        employer = Employer.objects.get(email=self.request.user.email)
        serializer.save(created_by=employer)



class VacancyDeleteAPIView(generics.DestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'  # Указываем, что идентификатор будет 'id', а не 'pk'

    def get_queryset(self):
        # Ограничиваем выборку вакансиями, созданными текущим пользователем
        return super().get_queryset().filter(created_by=self.request.user)
    @swagger_auto_schema(
    operation_summary="Удаление вакансии",
    operation_description=(
        "Позволяет авторизованному пользователю удалить вакансию. "
        "Удалять можно только те вакансии, которые создал текущий пользователь. "
        "Попытка удалить чужую вакансию вызовет ошибку."
    ),
    responses={
        status.HTTP_204_NO_CONTENT: openapi.Response(
            description="Вакансия успешно удалена."
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="Попытка удаления чужой вакансии или ее отсутствие",
            examples={
                "application/json": {"detail": "Вы не имеете права удалять эту вакансию."}
            },
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            description="Ошибка авторизации. Пользователь не авторизован.",
            examples={
                "application/json": {
                    "detail": "Учетные данные не были предоставлены."
                }
            },
        ),
    },
)
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


    
class VacancyUpdateView(generics.UpdateAPIView):
    queryset = Vacancy.objects.all()  
    serializer_class = VacancySerializer  
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Переопределяем get_object, чтобы добавить проверку прав пользователя"""
        obj = super().get_object()
        if obj.created_by.id != self.request.user.id:
            raise PermissionDenied("Вы не имеете права редактировать эту вакансию.")
        return obj
    @swagger_auto_schema(
        operation_summary="Обновление вакансии со всеми полями",
        operation_description="Позволяет авторизованному пользователю обновить вакансию. Необходимо указать все обязательные поля. Попытка обновить вакансию, не принадлежащую пользователю, вызовет ошибку.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=properties_for_vacancies,
            required=["title", "description", "work_conditions", "salary", "location", "number_of_openings", "skills", "status"],
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Вакансия успешно обновлена.",
                examples={
                    "application/json": {
    "id": 1,
    "title": "Тест",
    "description": "Описание вакансии для теста.",
    "work_conditions": {
        "format": "onsite",
        "employment_type": "full_time"
    },
    "salary": {
        "min_salary": 50000,
        "max_salary": 70000,
        "currency": "RUB"
    },
    "location": {
        "city": "Москва",
        "address": "Улица фронтендеров, 69"
    },
    "number_of_openings": 1,
    "skills": {
        "experience": "1",
        "tags": [
            "Python",
            "Дружелюбность"
        ],
        "languages": [
            "Русский",
            "Английский"
        ]
    },
    "publication_date": "2024-11-23T14:09:54.830327+03:00",
    "status": "published",
    "created_by": 2
}
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Ошибка в данных запроса.",
                examples={
                    "application/json": {
                        "title": ["Это поле не может быть пустым."]
                    }
                }
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Ошибка авторизации. Пользователь не авторизован.",
                examples={"application/json": {"detail": "Учетные данные не были предоставлены."}},
            ),
            status.HTTP_403_FORBIDDEN: openapi.Response(
                description="Запрещено. Попытка обновить чужую вакансию.",
                examples={"application/json": {"detail": "Вы не можете редактировать чужую вакансию."}},
            ),
        },
    )
    def put(self, request, *args, **kwargs):
        """
        Обрабатывает полный запрос обновления (PUT).
        """
        instance = self.get_object()
        
        required_fields = {
            "title",
            "description",
            "work_conditions",
            "salary",
            "location",
            "number_of_openings",
            "skills",
            "status",
        }

        missing_fields = required_fields - set(request.data.keys())
        if missing_fields:
            return Response(
                {"detail": f"Отсутствуют обязательные поля: {', '.join(missing_fields)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
    operation_summary="Частичное обновление вакансии",
    operation_description="Позволяет авторизованному пользователю частично обновить вакансию. Можно передавать только те поля, которые необходимо изменить. Попытка обновить вакансию, не принадлежащую пользователю, вызовет ошибку.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=properties_for_vacancies,  
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Вакансия успешно обновлена.",
            examples={
                "application/json": {
                    "id": 1,
                    "title": "Тест",
                    "description": "Обновленное описание вакансии.",
                    "work_conditions": {
                        "format": "onsite",
                        "employment_type": "full_time"
                    },
                    "salary": {
                        "min_salary": 50000,
                        "max_salary": 70000,
                        "currency": "RUB"
                    },
                    "location": {
                        "city": "Москва",
                        "address": "Улица фронтендеров, 69"
                    },
                    "number_of_openings": 1,
                    "skills": {
                        "experience": "1",
                        "tags": [
                            "Python",
                            "Дружелюбность"
                        ],
                        "languages": [
                            "Русский",
                            "Английский"
                        ]
                    },
                    "publication_date": "2024-11-23T14:09:54.830327+03:00",
                    "status": "published",
                    "created_by": 2
                }
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="Ошибка в данных запроса.",
            examples={
                "application/json": {
                    "detail": ""
                }
            }
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            description="Ошибка авторизации. Пользователь не авторизован.",
            examples={"application/json": {"detail": "Учетные данные не были предоставлены."}},
        ),
        status.HTTP_403_FORBIDDEN: openapi.Response(
            description="Запрещено. Попытка обновить чужую вакансию.",
            examples={"application/json": {"detail": "Вы не можете редактировать чужую вакансию."}},
        ),
    },
)
    def patch(self, request, *args, **kwargs):
        """
        Обрабатывает частичный запрос обновления (PATCH).
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    










