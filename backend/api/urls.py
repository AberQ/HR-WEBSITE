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



    path('api/applicant/vacancies/', VacancyListAPIView.as_view(), name='vacancy-list'),
    path('api/applicant/vacancies/<int:id>/', VacancyDetailAPIView.as_view(), name='vacancy-detail'),
    path('api/employer/<int:employer_id>/vacancies/', VacancyListByEmployerAPIView.as_view(), name='employer-vacancies'),



    
    path('api/employer/vacancies/create/', VacancyCreateAPIView.as_view(), name='vacancy-create'),  # POST запросы


    path('api/employer/vacancies/<int:pk>/edit/', VacancyUpdateView.as_view(), name='vacancy-edit'),

    path('api/employer/vacancies/<int:id>/delete', VacancyDeleteAPIView.as_view(), name='vacancy-delete'),


    path('api/applicant/resumes', UserResumeListView.as_view(), name='user-resume-list'),
    path('api/applicant/resumes/<int:pk>/', UserResumeDetailView.as_view(), name='user-resume-detail'),

    path('api/applicant/resumes/create/', UserResumeCreateView.as_view(), name='user-resume-create'),

    path('api/applicant/resumes/<int:pk>/delete/', ResumeDeleteAPIView.as_view(), name='resume-delete'),
    path('api/applicant/resumes/<int:pk>/update/', ResumeUpdateAPIView.as_view(), name='resume-update'),
]
