from django.urls import path
from registration.views import register
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api.views import *
from django.contrib import admin
from django.urls import path, include
from registration.views import *
schema_view = get_schema_view(
    openapi.Info(
        title="Job Vacancy API",
        default_version='v1',
        description="API documentation for job vacancies",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/vacancies/', VacancyListAPIView.as_view(), name='vacancy-list'),
    path('', home, name='home'),  # Определение маршрута с именем 'home'
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('admin/', admin.site.urls),
    path('api/vacancies/create/', VacancyCreateAPIView.as_view(), name='vacancy-create'),  # POST запросы
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
