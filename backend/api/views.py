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
    ]
  },
  "publication_date": "2024-11-11T17:52:37.802532+03:00",
  "status": "published",
  "created_by": 2
},
{
  "id": 2,
  "title": "Frontend",
  "description": "Описание вакансии для теста.",
  "work_conditions": {
    "format": "hybrid",
    "employment_type": "part_time"
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
    ]
  },
  "publication_date": "2024-11-11T17:52:37.802532+03:00",
  "status": "archived",
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
    ]
  },
  "publication_date": "2024-11-11T17:52:37.802532+03:00",
  "status": "published",
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
                                ]
                            },
                            "publication_date": "2024-11-12T09:04:51.269465+03:00",
                            "status": "Published",
                            "created_by": 2
                        },
                        {
                            "id": 2,
                            "title": "Backend Developer",
                            "description": "Нету ID",
                            "work_conditions": {
                                "format": "remote",
                                "employment_type": "full_time"
                            },
                            "salary": {
                                "min_salary": 60000,
                                "max_salary": 120000,
                                "currency": "RUB"
                            },
                            "location": {
                                "city": "Санкт-Петербург",
                                "address": "ул. Невский проспект, д. 15"
                            },
                            "number_of_openings": 3,
                            "skills": {
                                "experience": "1-3",
                                "tech_stack_tags": []
                            },
                            "publication_date": "2024-11-13T16:49:03.977315+03:00",
                            "status": "checking",
                            "created_by": 2
                        },
                        # Добавьте сюда другие вакансии, если нужно
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
        operation_description="Создание новой вакансии. Требуется авторизация работодателем",
        request_body=VacancySerializerForCreateAPI,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Вакансия успешно создана.",
                examples={
                    "application/json": {
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
      ]
    },
    "publication_date": "2024-11-12T09:04:51.269465+03:00",
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
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            # Проверка, что пользователь является экземпляром Applicant
            applicant = Applicant.objects.get(email=self.request.user.email)
            serializer.save(applicant=applicant)
        except ObjectDoesNotExist:
            raise ValidationError("Только соискатели могут создавать резюме.")
        

class ResumeDeleteAPIView(generics.DestroyAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

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

    def get_object(self):
        # Получаем резюме, которое принадлежит текущему пользователю
        resume = super().get_object()
        # Проверяем, является ли резюме принадлежащим текущему пользователю (или его аппликанту)
        if resume.applicant.email != self.request.user.email:
            raise PermissionDenied("Вы не можете редактировать чужое резюме.")
        return resume

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # partial=True позволяет обновлять только часть полей

        # Проверяем валидность данных
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)