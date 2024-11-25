from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect, render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import *
from .forms import CustomAuthenticationForm
from .models import *
from .serializers import *


def applicant_registration(request):
    if request.method == "POST":
        form = ApplicantSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # сохранение номера
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=user.email, password=raw_password)
            login(request, user)
            return redirect("/test/")
    else:
        form = ApplicantSignUpForm()
    return render(request, "signup.html", {"form": form})


def employer_registration(request):
    if request.method == "POST":
        form = EmployerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # сохранение номера
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=user.email, password=raw_password)
            login(request, user)
            return redirect("/test/")
    else:
        form = EmployerSignUpForm()
    return render(request, "signup.html", {"form": form})


def custom_login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.user_cache  # Получаем пользователя из кэша
            login(request, user)
            return redirect("home")
    else:
        form = CustomAuthenticationForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)  # Выход из учетной записи
    return redirect("home")  # Перенаправление на главную страницу или другую страницу


def choice_registration(request):
    return render(request, "choice_registration.html")


from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer





# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# API для регистрации
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

User = get_user_model()


class RegisterApplicantView(generics.CreateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer


    
    @swagger_auto_schema(
    operation_summary="Регистрация нового соискателя",
    operation_description=(
        "Эндпоинт позволяет зарегистрировать нового соискателя. "
        "Необходимы данные в формате JSON. После успешной регистрации возвращаются данные нового пользователя."
    ),
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Email соискателя",
                example="applicant@example.com",
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Пароль для аккаунта",
                example="secure_password_123",
            ),
            "first_name": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Имя соискателя",
                example="Иван",
            ),
            "last_name": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Фамилия соискателя",
                example="Иванов",
            ),
            "patronymic": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Отчество соискателя (необязательное поле)",
                example="Иванович",
            ),
        },
        required=["email", "password", "first_name", "last_name"],
        example={
            "email": "applicant@example.com",
            "password": "secure_password_123",
            "first_name": "Иван",
            "last_name": "Иванов",
            "patronymic": "Иванович",
        },
    ),
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            description="Успешная регистрация",
            examples={
                "application/json": {
                                    "id": 4,
                                    "email": "applicant1@example.com",
                                    "password": "pbkdf2_sha256$870000$qWRm0EZcOyMM0n9K7UnXdy$P3zC2BRlO3weY1jX0Y8F1r5jqk/E4TdkrEzfiTdkTUw=",
                                    "first_name": "Иван",
                                    "last_name": "Иванов",
                                    "patronymic": "Иванович"
                                    }
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="Ошибка валидации данных",
            examples={
                "application/json": {
                    "error": "Поле 'email' обязательно для заполнения."
                }
            }
        ),
    },
)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegisterEmployerView(generics.CreateAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получить профиль текущего пользователя",
        operation_description="Отдает данные об текущем аккаунте в сессии",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Данные профиля пользователя",
                examples={
                    "application/json": {
                        "Комментарий_1": "Это ответ для работодателя",
                        "Данные JSON_1": {
                            "id": 4,
                            "email": "egor.master2017@gmail.com",
                            "password": "pbkdf2_sha256$870000$q7DMV9gwjew5Xr82Cnewyz$gQK11gcSWIrjIOZSc/O5ZXc5rWsst/hUbE7Y2/u5tNI=",
                            "company_name": "Arapov-Indasrize",
                            "company_info": "",
                        },
                        "Комментарий_2": "Это ответ для соискателя",
                        "Данные JSON_2": {
                            "id": 3,
                            "email": "applicant@example.com",
                            "password": "pbkdf2_sha256$870000$oOVbHvCpEEyoRUDVbBPRE8$3hiQeqz3FCc5q68p99XNyG3IUSfnk0S00/J4l/f3EB0=",
                            "first_name": "John",
                            "last_name": "Doe",
                            "patronymic": "Ivanovich",
                        },
                    }
                },
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Профиль пользователя не найден",
                examples={
                    "application/json": {
                        "error": "Учетные данные не были предоставлены."
                    }
                },
            ),
        },
    )
    def get(self, request):
        user = request.user

        # Определяем, является ли пользователь соискателем или работодателем
        if hasattr(user, "applicant"):
            serializer = ApplicantSerializer(user.applicant)
        elif hasattr(user, "employer"):
            serializer = EmployerSerializer(user.employer)
        else:
            return Response({"detail": "Профиль пользователя не найден"}, status=404)

        return Response(serializer.data)
