from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from .forms import CustomAuthenticationForm
from django.contrib.auth import authenticate, login

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Замените 'home' на нужный URL
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})