from rest_framework import generics
from .models import Vacancy
from .serializers import VacancySerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Vacancy
from .serializers import VacancySerializer
from django.shortcuts import render
class VacancyListAPIView(generics.ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

class VacancyCreateAPIView(generics.CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

def home(request):
    return render(request, 'home.html')