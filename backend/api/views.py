from rest_framework import generics
from .models import Vacancy
from .serializers import VacancySerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Vacancy
from .serializers import VacancySerializer
from django.shortcuts import render
from registration.views import *
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
class VacancyListAPIView(generics.ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [IsAuthenticated]
class VacancyCreateAPIView(generics.CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


def home(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

from django.shortcuts import render
from .models import Vacancy
@login_required
def vacancy_list(request):
    vacancies = Vacancy.objects.filter(status='published')  # Фильтрация по статусу
    return render(request, 'vacancy_list.html', {'vacancies': vacancies})

def redirect_to_api_vacancyes_create(request):
    return redirect('/api/vacancies/create')