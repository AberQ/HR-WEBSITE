from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import *
def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # сохранение номера
            Profile_employee.objects.create(user=user)
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})