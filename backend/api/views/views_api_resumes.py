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
from rest_framework import status
from .swagger_properties import *
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#API для резюме
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



class UserResumeListView(generics.ListAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получить список резюме текущего пользователя",
        operation_description=(
            "Эндпоинт возвращает список резюме текущего пользователя, если он является аппликантом. "
            "Пользователи с другим типом учетной записи получат ошибку доступа."
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Список резюме текущего пользователя",
                examples={
                    "application/json": [
    {
        "id": 1,
        "desired_position": "Junior Python Developer",
        "candidate_name": "Тест Тестов",
        "content": "Контент",
        "contacts": {
            "email": "applicant@example.com",
            "phone": "+7 123 456 7890"
        },
        "location": {
            "city": "Москва"
        },
        "degree": "bachelor",
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
        "portfolio_link": "https://github.com/AberQ/HR-WEBSITE",
        "updated_at": "2024-11-19T21:06:28.912052+03:00",
        "applicant": 3
    },
    {
        "id": 2,
        "desired_position": "Junior Python Developer",
        "candidate_name": "Тест Тестов",
        "content": "rgrg",
        "contacts": {
            "email": "applicant@example.com",
            "phone": "+7 123 456 7890"
        },
        "location": {
            "city": "Москва"
        },
        "degree": "bachelor",
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
        "portfolio_link": "https://github.com/AberQ/HR-WEBSITE",
        "updated_at": "2024-11-19T22:51:06.319919+03:00",
        "applicant": 3
    }
]
                }
            ),
            status.HTTP_403_FORBIDDEN: openapi.Response(
                "Доступ запрещен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Сообщение об ошибке доступа",
                            example="Только пользователи-аппликанты могут просматривать резюме."
                        )
                    }
                )
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                "Неавторизованный доступ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Сообщение об ошибке авторизации",
                            example="Учетные данные не были предоставлены."
                        )
                    }
                )
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Возвращает список резюме текущего пользователя.
        """
        return super().get(request, *args, **kwargs)
    

    def get_queryset(self):
        
        user = self.request.user
        print("Текущий пользователь:", self.request.user)
        
        if not hasattr(user, 'applicant'):
            raise PermissionDenied("Только пользователи-аппликанты могут просматривать резюме.")
        
        
        return Resume.objects.filter(applicant=user)
    
class UserResumeDetailView(generics.RetrieveAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получить конкретное резюме текущего пользователя",
        operation_description=(
            "Эндпоинт возвращает конкретное резюме текущего пользователя, если он является соискателем. "
            "Пользователи с другим типом учетной записи получат ошибку доступа."
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Конкретное резюме текущего пользователя",
                examples={
                    "application/json": [
    {
    "id": 1,
    "desired_position": "Junior Python Developer",
    "candidate_name": "Тест Тестов",
    "content": "Контент",
    "contacts": {
        "email": "applicant@example.com",
        "phone": "+7 123 456 7890"
    },
    "location": {
        "city": "Москва"
    },
    "degree": "bachelor",
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
    "portfolio_link": "https://github.com/AberQ/HR-WEBSITE",
    "updated_at": "2024-11-19T21:06:28.912052+03:00",
    "applicant": 3
}
]
                }
            ),
            status.HTTP_403_FORBIDDEN: openapi.Response(
                "Доступ запрещен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Сообщение об ошибке доступа",
                            example="Только пользователи-аппликанты могут просматривать резюме."
                        )
                    }
                )
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                "Неавторизованный доступ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Сообщение об ошибке авторизации",
                            example="Учетные данные не были предоставлены."
                        )
                    }
                )
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Обработчик GET-запроса для получения резюме.
        """
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        
        user = self.request.user
       
        if not hasattr(user, 'applicant'):
            raise PermissionDenied("Только пользователи-аппликанты могут просматривать резюме.")
        
        # Фильтруем резюме по текущему пользователю
        return Resume.objects.filter(applicant=user)
    

class UserResumeCreateView(generics.CreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializerForCreateAPI
    permission_classes = [permissions.IsAuthenticated]


    @swagger_auto_schema(
        operation_summary="Создать новое резюме для текущего пользователя",
        operation_description=(
            "Эндпоинт позволяет зарегистрированному пользователю создать резюме, "
            "если он является соискателем. Другие типы учетных записей получат ошибку."
        ),
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["desired_position", "contacts", "location", "content", 'degree', 'skills', 'candidate_name'],
        properties=properties_for_resume
    ),
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Резюме успешно создано",
                examples={
                    "application/json": 
                    {
                        "id": 2,
                        "desired_position": "Junior Python Developer",
                        "candidate_name": "Тест Тестов",
                        "content": "rgrg",
                        "contacts": {
                            "email": "applicant@example.com",
                            "phone": "+7 123 456 7890"
                        },
                        "location": {
                            "city": "Москва"
                        },
                        "degree": "bachelor",
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
                        "portfolio_link": "https://github.com/AberQ/HR-WEBSITE",
                        "updated_at": "2024-11-19T22:51:06.319919+03:00"
                    }

                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Ошибка валидации",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Сообщение об ошибке",
                            example="Только соискатели могут создавать резюме."
                        )
                    }
                )
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Неавторизованный доступ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Сообщение об ошибке авторизации",
                            example="Учетные данные не были предоставлены."
                        )
                    }
                )
            ),
            status.HTTP_403_FORBIDDEN: openapi.Response(
                description="Запрещено",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Сообщение об ошибке",
                            example="Только соискатели могут создавать резюме."
                        )
                    }
                )
            )
        }
    )
        
    def post(self, request, *args, **kwargs):
        """
        Обработчик POST-запроса для создания резюме.
        """
        return super().post(request, *args, **kwargs)



    def perform_create(self, serializer):
        try:
            # Проверка, что пользователь является экземпляром Applicant
            applicant = Applicant.objects.get(email=self.request.user.email)
            
            # Сохраняем резюме с данными пользователя
            resume = serializer.save(applicant=applicant)

            # Обрабатываем ManyToMany поля вручную
            # Для languages
            if 'languages' in self.request.data:
                languages = self.request.data.get('languages', [])
                for language_name in languages:
                    language, created = Language.objects.get_or_create(name=language_name)
                    resume.languages.add(language)

            # Для tags
            if 'tags' in self.request.data:
                tags = self.request.data.get('tags', [])
                for tag_name in tags:
                    tech_stack_tag, created = Tag.objects.get_or_create(name=tag_name)
                    resume.tags.add(tech_stack_tag)

            resume.save()
        except Applicant.DoesNotExist:
        # Выбрасываем исключение с кодом 403
            raise PermissionDenied("Только соискатели могут создавать резюме.")
        

class ResumeDeleteAPIView(generics.DestroyAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        
        operation_summary="Удаление резюме",
        operation_description="Позволяет авторизованному пользователю удалить свое резюме. "
                               "Попытка удалить чужое резюме вызовет ошибку.",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description="Резюме успешно удалено.",
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Ошибка авторизации. Пользователь не авторизован.",
                examples={"application/json": {"detail": "Учетные данные не были предоставлены."}},
            ),
            status.HTTP_403_FORBIDDEN: openapi.Response(
                description="Запрещено. Попытка удалить чужое резюме.",
                examples={"application/json": {"detail": "Вы не можете удалить чужое резюме."}},
            ),
        },
    )
    def delete(self, request, *args, **kwargs):
        # Получаем объект, который нужно удалить
        instance = self.get_object()

        # Преобразуем request.user в объект Applicant, если это необходимо
        applicant = instance.applicant

        # Если email в запросе отличается от email в applicant, запрещаем удаление
        if applicant.email != request.user.email:
            raise PermissionDenied("Вы не можете удалить чужое резюме.")

        # Удаляем резюме
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


    def perform_destroy(self, instance):
        # Преобразуем request.user в объект Applicant, если это необходимо
        applicant = instance.applicant

        # Если email в запросе отличается от email в applicant, запрещаем удаление
        if applicant.email != self.request.user.email:
            raise PermissionDenied("Вы не можете удалить чужое резюме.")

        # Удаляем резюме
        instance.delete()



class ResumeUpdateAPIView(UpdateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
    operation_summary="Обновление резюме со всеми полями",
    operation_description="Позволяет авторизованному пользователю обновить свое резюме. Попытка обновить чужое резюме вызовет ошибку. Указывать нужно ВСЕ поля.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=properties_for_resume,
        required=["desired_position", "candidate_name", "contacts", "location", "degree", "skills", "portfolio_link"],
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Резюме успешно обновлено.",
            examples={
                "application/json": {
                    "id": 1,
                    "desired_position": "Junior Python Developer",
                    "candidate_name": "Тест Тестов",
                    "content": "Контент",
                    "contacts": {
                        "email": "applicant@example.com",
                        "phone": "+7 123 456 7890"
                    },
                    "location": {
                        "city": "Москва"
                    },
                    "degree": "bachelor",
                    "skills": {
                        "experience": "1",
                        "tags": ["Python", "Дружелюбность"],
                        "languages": ["Русский", "Английский"]
                    },
                    "portfolio_link": "https://github.com/AberQ/HR-WEBSITE",
                    "updated_at": "2024-11-21T21:46:10.723536+03:00",
                    "applicant": 3
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
            description="Запрещено. Попытка обновить чужое резюме.",
            examples={"application/json": {"detail": "Вы не можете редактировать чужое резюме."}},
        ),
    },
)



    def put(self, request, *args, **kwargs):
        """
        Обрабатывает полный запрос обновления (PUT).
        """
        instance = self.get_object()
        # Проверяем, содержит ли запрос все обязательные поля
        required_fields = {
            "desired_position",
            "candidate_name",
            "contacts",
            'content',
            "location",
            "degree",
            'skills',
            "portfolio_link"
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
        operation_summary="Обновление части полей в резюме",
        operation_description="Позволяет авторизованному пользователю обновить свое резюме. Попытка обновить чужое резюме вызовет ошибку."
                               "Можно указывать только желаемые поля. ",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=properties_for_resume,
        
    ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Резюме успешно обновлено.",
                examples={
                    "application/json": {
                    "id": 1,
                    "desired_position": "Junior Python Developer",
                    "candidate_name": "Тест Тестов",
                    "content": "Контент",
                    "contacts": {
                        "email": "applicant@example.com",
                        "phone": "+7 123 456 7890"
                    },
                    "location": {
                        "city": "Москва"
                    },
                    "degree": "bachelor",
                    "skills": {
                        "experience": "1",
                        "tags": ["Python", "Дружелюбность"],
                        "languages": ["Русский", "Английский"]
                    },
                    "portfolio_link": "https://github.com/AberQ/HR-WEBSITE",
                    "updated_at": "2024-11-21T21:46:10.723536+03:00",
                    "applicant": 3
                }
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Ошибка в данных запроса.",
                examples={
                    "application/json": {
                        "title": ["Значения нет среди допустимых вариантов"]
                    }
                }
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Ошибка авторизации. Пользователь не авторизован.",
                examples={"application/json": {"detail": "Учетные данные не были предоставлены."}},
            ),
            status.HTTP_403_FORBIDDEN: openapi.Response(
                description="Запрещено. Попытка обновить чужое резюме.",
                examples={"application/json": {"detail": "Вы не можете редактировать чужое резюме."}},
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
    

    def get_object(self):
        # Получаем резюме, которое принадлежит текущему пользователю
        resume = super().get_object()
        # Проверяем, является ли резюме принадлежащим текущему пользователю (или его аппликанту)
        if resume.applicant.email != self.request.user.email:
            raise PermissionDenied("Вы не можете редактировать чужое резюме.")
        return resume
    
