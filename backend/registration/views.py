from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomAuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import redirect




def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # сохранение номера
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.email, password=raw_password)
            login(request, user)
            return redirect('/test/')
    else:
        form = SignUpForm()
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


# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer  # Создадим сериализатор ниже

User = get_user_model()

@api_view(['POST'])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
