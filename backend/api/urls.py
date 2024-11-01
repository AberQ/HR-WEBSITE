from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api.views import *
from django.contrib import admin
from django.urls import path, include
from registration.views import *

urlpatterns = [
    path('test/', home, name='home'),
    path('test/contact', contact, name='contact'),
    path('test/vacancies/', vacancy_list, name='vacancy_list'),
    path('test/add/', add_vacancy, name='add_vacancy'),
    path('api/vacancies/', VacancyListAPIView.as_view(), name='vacancy-list'),
    path('api/vacancies/<int:id>/', VacancyDetailAPIView.as_view(), name='vacancy-detail'),
    path('api/vacancies/create/', VacancyCreateAPIView.as_view(), name='vacancy-create'),  # POST запросы
]
