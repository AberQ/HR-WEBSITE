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
    path('registration/', registration, name='registration'),
    path('login/', custom_login_view, name='login'),
    path('logout/', logout_view, name='logout'),  
    path('api/registration/', register_user, name='register_user'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]