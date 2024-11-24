from django.urls import path

from api.views.views_api_resumes import *
from api.views.views_api_tags import *
from api.views.views_api_vacancies import *
from api.views.views_test import *
from registration.views import *

urlpatterns = [
    path("test/", home, name="home"),
    path("test/contact", contact, name="contact"),
    path("test/vacancies/", vacancy_list, name="vacancy_list"),
    path("test/add/", add_vacancy, name="add_vacancy"),
    path("api/tags/", TagListAPIView.as_view(), name="tag_list"),
    path("api/tags/create/", TagCreateView.as_view(), name="create_tag"),
    path("api/applicant/vacancies/", VacancyListAPIView.as_view(), name="vacancy_list"),
    path(
        "api/applicant/vacancies/<int:id>/",
        VacancyDetailAPIView.as_view(),
        name="vacancy_detail",
    ),
    path(
        "api/employer/<int:employer_id>/vacancies/",
        VacancyListByEmployerAPIView.as_view(),
        name="employer_vacancies",
    ),
    path(
        "api/employer/vacancies/create/",
        VacancyCreateAPIView.as_view(),
        name="vacancy_create",
    ),  # POST запросы
    path(
        "api/employer/vacancies/<int:pk>/edit/",
        VacancyUpdateView.as_view(),
        name="vacancy_edit",
    ),
    path(
        "api/employer/vacancies/<int:id>/delete",
        VacancyDeleteAPIView.as_view(),
        name="vacancy_delete",
    ),
    path(
        "api/applicant/resumes", UserResumeListView.as_view(), name="user-resume-list"
    ),
    path(
        "api/applicant/resumes/<int:pk>/",
        UserResumeDetailView.as_view(),
        name="user-resume-detail",
    ),
    path(
        "api/applicant/resumes/create/",
        UserResumeCreateView.as_view(),
        name="user-resume-create",
    ),
    path(
        "api/applicant/resumes/<int:pk>/delete/",
        ResumeDeleteAPIView.as_view(),
        name="resume-delete",
    ),
    path(
        "api/applicant/resumes/<int:pk>/edit/",
        ResumeUpdateAPIView.as_view(),
        name="resume-update",
    ),
]
