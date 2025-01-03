from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.views.views_api_vacancies import *
from registration.views import *

schema_view = get_schema_view(
    openapi.Info(
        title="Job Vacancy API",
        default_version="v1",
        description="API documentation for job vacancies",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="egor.master2017@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # Разрешаем доступ к Swagger UI
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("select2/", include("django_select2.urls")),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("", include("api.urls")),  # Подключаем urls из приложения api
    path("", include("registration.urls")),  # Подключаем urls из приложения api
]
