from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api.views import *
from django.contrib import admin
from django.urls import path, include
from registration.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('applicant_registration/', applicant_registration, name='applicant_registration'),
    path('employer_registration/', employer_registration, name='employer_registration'),
    path('login/', custom_login_view, name='login'),
    path('logout/', logout_view, name='logout'),  
    path('choice_registration', choice_registration, name='choice_registration'),
    path('api/register/applicant', RegisterApplicantView.as_view(), name='register_applicant'),
    path('api/register/employer', RegisterEmployerView.as_view(), name='register_employer'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]