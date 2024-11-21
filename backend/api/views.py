from rest_framework import generics
from .models import Vacancy
from .serializers import *
from rest_framework import generics
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework import status
from .models import Vacancy
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from registration.views import *
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from registration.forms import VacancyForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Vacancy
from rest_framework import permissions
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Vacancy
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

def home(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')


@login_required
def vacancy_list(request):
    # Проверка, является ли пользователь Applicant
    if not hasattr(request.user, 'applicant'):
        return render(request, 'access_denied.html')  # Показать страницу доступа запрещен
    
    vacancies = Vacancy.objects.filter(status='published')  # Фильтрация по статусу
    return render(request, 'vacancy_list.html', {'vacancies': vacancies})






@login_required
def add_vacancy(request):
    # Проверка, является ли пользователь Employer
    try:
        employer = request.user.employer  # Получаем экземпляр Employer, связанный с текущим пользователем
    except Employer.DoesNotExist:
        return render(request, 'access_denied.html')  # Показать страницу доступа запрещен

    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)  # Не сохраняем сразу
            vacancy.created_by = employer  # Устанавливаем текущего работодателя как создателя вакансии
            vacancy.save()  # Сохраняем вакансию
            return redirect('vacancy_list')  # Переход к списку вакансий после успешного сохранения
    else:
        form = VacancyForm()  # Создаем пустую форму для отображения

    return render(request, 'add_vacancy.html', {'form': form})  # Отображаем форму для добавления вакансии

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
            "tech_stack_tags": [
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
            "tech_stack_tags": [
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
        "tech_stack_tags": [
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
            "tech_stack_tags": [
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
            "tech_stack_tags": [
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
        request_body=VacancySerializerForCreateAPI,
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
        "tech_stack_tags": [
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

    def perform_destroy(self, instance):
        #print("Автор вакансии:", instance.created_by)
        #print("Текущий пользователь:", self.request.user)
        # Проверяем, что текущий пользователь — автор вакансии
        if instance.created_by.id != self.request.user.id:
            raise PermissionDenied("Вы не имеете права удалять эту вакансию.")
        # Вызываем метод удаления, если проверка пройдена
        super().perform_destroy(instance)


    
class VacancyUpdateView(generics.UpdateAPIView):
    queryset = Vacancy.objects.all()  # Должен быть указан queryset для поиска объекта
    serializer_class = VacancySerializer  # Сериализатор, который будет использоваться для обновления
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Переопределяем get_object, чтобы добавить проверку прав пользователя"""
        obj = super().get_object()
        if obj.created_by.id != self.request.user.id:
            raise PermissionDenied("Вы не имеете права редактировать эту вакансию.")
        return obj

    def perform_update(self, serializer):
        """Переопределяем perform_update, чтобы автоматически установить created_by"""
        # Устанавливаем created_by на основе текущего пользователя
        employer = Employer.objects.get(email=self.request.user.email)
        serializer.save(created_by=employer)  # Устанавливаем создателя вакансии

    def put(self, request, *args, **kwargs):
        """Используем встроенную логику put"""
        return super().put(request, *args, **kwargs)
    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#API для резюме
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



from rest_framework import status

class TechStackTagCreateView(CreateAPIView):
    queryset = TechStackTag.objects.all()
    serializer_class = TechStackTagSerializer

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
                TechStackTagSerializer
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
            "tech_stack_tags": [
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
            "tech_stack_tags": [
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
        # Получаем текущего пользователя из запроса
        user = self.request.user
        print("Текущий пользователь:", self.request.user)
        # Проверяем, является ли пользователь экземпляром `Applicant`
        if not hasattr(user, 'applicant'):
            raise PermissionDenied("Только пользователи-аппликанты могут просматривать резюме.")
        
        # Фильтруем резюме по текущему пользователю
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
        "tech_stack_tags": [
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
        # Получаем текущего пользователя
        user = self.request.user
        # Проверяем, является ли пользователь аппликантом
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
        properties={
            "desired_position": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Желаемая должность",
                example="Junior Python Developer"
            ),
            "candidate_name": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Имя кандидата",
                example="Тест Тестов"
            ),
            "content": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Описание кандидата или сопроводительный текст",
                example="Меня зовут Тест, я увлекаюсь Python и создаю проекты на Django."
            ),
            "contacts": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=["email", "phone"],
                properties={
                    "email": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_EMAIL,
                        description="Email соискателя",
                        example="applicant@example.com"
                    ),
                    "phone": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Телефон соискателя",
                        example="+7 123 456 7890"
                    )
                },
                description="Контактная информация"
            ),
            "location": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=["city"],
                properties={
                    "city": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Город проживания",
                        example="Москва"
                    )
                },
                description="Информация о местоположении"
            ),
            "degree": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Уровень образования",
                example="bachelor"
            ),
            "skills": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "experience": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Опыт работы в годах",
                        example="1"
                    ),
                    "tech_stack_tags": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_STRING),
                        description="Навыки из технического стека",
                        example=["Python", "Дружелюбность"]
                    ),
                    "languages": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_STRING),
                        description="Языки, которыми владеет соискатель",
                        example=["Русский", "Английский"]
                    )
                },
                description="Навыки кандидата"
            ),
            "portfolio_link": openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_URI,
                description="Ссылка на портфолио",
                example="https://github.com/AberQ/HR-WEBSITE"
            )
        }
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
                            "tech_stack_tags": [
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

            # Для tech_stack_tags
            if 'tech_stack_tags' in self.request.data:
                tech_stack_tags = self.request.data.get('tech_stack_tags', [])
                for tag_name in tech_stack_tags:
                    tech_stack_tag, created = TechStackTag.objects.get_or_create(name=tag_name)
                    resume.tech_stack_tags.add(tech_stack_tag)

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
        properties={
            "desired_position": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Желаемая должность кандидата",
                example="Junior Python Developer"
            ),
            "candidate_name": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="ФИО кандидата",
                example="Тест Тестов"
            ),
            "content": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Описание кандидата или сопроводительный текст",
                example="Меня зовут Тест, я увлекаюсь Python и создаю проекты на Django."
            ),
            "contacts": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=["email", "phone"],
                properties={
                    "email": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_EMAIL,
                        description="Email кандидата",
                        example="applicant@example.com"
                    ),
                    "phone": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Телефон кандидата",
                        example="+7 123 456 7890"
                    )
                },
                description="Контактная информация кандидата"
            ),
            "location": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=["city"],
                properties={
                    "city": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Город проживания кандидата",
                        example="Москва"
                    )
                },
                description="Местоположение кандидата"
            ),
            "degree": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Уровень образования кандидата",
                example="bachelor"
            ),
            "skills": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "experience": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Количество лет опыта работы",
                        example="1"
                    ),
                    "tech_stack_tags": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_STRING),
                        description="Технические навыки кандидата",
                        example=["Python", "Дружелюбность"]
                    ),
                    "languages": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_STRING),
                        description="Языки, которыми владеет кандидат",
                        example=["Русский", "Английский"]
                    )
                },
                description="Навыки кандидата"
            ),
            "portfolio_link": openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_URI,
                description="Ссылка на портфолио кандидата",
                example="https://github.com/AberQ/HR-WEBSITE"
            ),
        },
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
                        "tech_stack_tags": ["Python", "Дружелюбность"],
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
        properties={
            "desired_position": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Желаемая должность кандидата",
                example="Junior Python Developer"
            ),
            "candidate_name": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="ФИО кандидата",
                example="Тест Тестов"
            ),
            "content": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Описание кандидата или сопроводительный текст",
                example="Меня зовут Тест, я увлекаюсь Python и создаю проекты на Django."
            ),
            "contacts": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=["email", "phone"],
                properties={
                    "email": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_EMAIL,
                        description="Email кандидата",
                        example="applicant@example.com"
                    ),
                    "phone": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Телефон кандидата",
                        example="+7 123 456 7890"
                    )
                },
                description="Контактная информация кандидата"
            ),
            "location": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=["city"],
                properties={
                    "city": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Город проживания кандидата",
                        example="Москва"
                    )
                },
                description="Местоположение кандидата"
            ),
            "degree": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Уровень образования кандидата",
                example="bachelor"
            ),
            "skills": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "experience": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Количество лет опыта работы",
                        example="1"
                    ),
                    "tech_stack_tags": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_STRING),
                        description="Технические навыки кандидата",
                        example=["Python", "Дружелюбность"]
                    ),
                    "languages": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_STRING),
                        description="Языки, которыми владеет кандидат",
                        example=["Русский", "Английский"]
                    )
                },
                description="Навыки кандидата"
            ),
            "portfolio_link": openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_URI,
                description="Ссылка на портфолио кандидата",
                example="https://github.com/AberQ/HR-WEBSITE"
            ),
        },
        required=["desired_position", "candidate_name", "contacts", "location", "degree", "skills", "portfolio_link"],
    ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Резюме успешно обновлено.",
                examples={
                    "application/json": {
                        "id": 1,
                        "title": "Новый заголовок",
                        "content": "Обновленное содержание",
                        "applicant": 2
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
    
