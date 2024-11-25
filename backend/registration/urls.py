from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api.views.views_api_vacancies import *
from registration.views import *

urlpatterns = [
    path('choice_registration/', choice_registration, name='choice_registration'),
    path('applicant_registration/', applicant_registration, name='applicant_registration'),
    path('employer_registration/', employer_registration, name='employer_registration'),
    

    path('login/', custom_login_view, name='login'),
    path('logout/', logout_view, name='logout'),  
    


    
    path('api/register/applicant', RegisterApplicantView.as_view(), name='register_applicant'),
    path('api/register/employer', RegisterEmployerView.as_view(), name='register_employer'),


    path('api/login/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/login/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    
]