from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomAuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from django.contrib.auth import get_user_model



def applicant_registration(request):
    if request.method == 'POST':
        form = ApplicantSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # сохранение номера
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.email, password=raw_password)
            login(request, user)
            return redirect('/test/')
    else:
        form = ApplicantSignUpForm()
    return render(request, 'signup.html', {'form': form})


def employer_registration(request):
    if request.method == 'POST':
        form = EmployerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # сохранение номера
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.email, password=raw_password)
            login(request, user)
            return redirect('/test/')
    else:
        form = EmployerSignUpForm()
    return render(request, 'signup.html', {'form': form})


def custom_login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.user_cache  # Получаем пользователя из кэша
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)  # Выход из учетной записи
    return redirect('home')  # Перенаправление на главную страницу или другую страницу

def choice_registration(request):
    return render(request, 'choice_registration.html')



User = get_user_model()



class RegisterApplicantView(generics.CreateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer

    def create(self, request, *args, **kwargs):
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