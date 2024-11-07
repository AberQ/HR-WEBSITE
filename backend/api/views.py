from rest_framework import generics
from .models import Vacancy
from .serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Vacancy
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from registration.views import *
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from registration.forms import VacancyForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Vacancy
from rest_framework import permissions
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Vacancy



def home(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')


@login_required
def vacancy_list(request):
    # Проверка, является ли пользователь Applicant
    if not hasattr(request.user, 'applicant'):
        return render(request, 'access_denied.html')  # Показать страницу доступа запрещен
    
    vacancies = Vacancy.objects.filter(status='published')  # Фильтрация по статусу
    return render(request, 'vacancy_list.html', {'vacancies': vacancies})






@login_required
def add_vacancy(request):
    # Проверка, является ли пользователь Employer
    try:
        employer = request.user.employer  # Получаем экземпляр Employer, связанный с текущим пользователем
    except Employer.DoesNotExist:
        return render(request, 'access_denied.html')  # Показать страницу доступа запрещен

    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)  # Не сохраняем сразу
            vacancy.created_by = employer  # Устанавливаем текущего работодателя как создателя вакансии
            vacancy.save()  # Сохраняем вакансию
            return redirect('vacancy_list')  # Переход к списку вакансий после успешного сохранения
    else:
        form = VacancyForm()  # Создаем пустую форму для отображения

    return render(request, 'add_vacancy.html', {'form': form})  # Отображаем форму для добавления вакансии

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#API для вакансий
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class VacancyListAPIView(generics.ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    #permission_classes = [permissions.IsAuthenticated]

class VacancyDetailAPIView(generics.RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    lookup_field = 'id'  # Используем 'id' для поиска вакансии по ID



class VacancyListByEmployerAPIView(generics.ListAPIView):
    serializer_class = VacancySerializer

    def get_queryset(self):
        employer_id = self.kwargs['employer_id']
        return Vacancy.objects.filter(created_by__id=employer_id)

    def get(self, request, *args, **kwargs):
        employer_id = self.kwargs['employer_id']
        try:
            vacancies = self.get_queryset()
            serializer = self.get_serializer(vacancies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Employer.DoesNotExist:
            return Response({'error': 'Работодатель не найден.'}, status=status.HTTP_404_NOT_FOUND)




class VacancyCreateAPIView(generics.CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializerForCreateAPI
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Убедитесь, что текущий пользователь является экземпляром Employer
        employer = Employer.objects.get(email=self.request.user.email)
        serializer.save(created_by=employer)  # Устанавливаем создателя вакансии



class VacancyDeleteAPIView(generics.DestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'  # Указываем, что идентификатор будет 'id', а не 'pk'

    def get_queryset(self):
        # Ограничиваем выборку вакансиями, созданными текущим пользователем
        return super().get_queryset().filter(created_by=self.request.user)

    def perform_destroy(self, instance):
        #print("Автор вакансии:", instance.created_by)
        #print("Текущий пользователь:", self.request.user)
        # Проверяем, что текущий пользователь — автор вакансии
        if instance.created_by.id != self.request.user.id:
            raise PermissionDenied("Вы не имеете права удалять эту вакансию.")
        # Вызываем метод удаления, если проверка пройдена
        super().perform_destroy(instance)


    
class VacancyUpdateView(generics.UpdateAPIView):
    queryset = Vacancy.objects.all()  # Должен быть указан queryset для поиска объекта
    serializer_class = VacancySerializer  # Сериализатор, который будет использоваться для обновления
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Переопределяем get_object, чтобы добавить проверку прав пользователя"""
        obj = super().get_object()
        if obj.created_by.id != self.request.user.id:
            raise PermissionDenied("Вы не имеете права редактировать эту вакансию.")
        return obj

    def perform_update(self, serializer):
        """Переопределяем perform_update, чтобы автоматически установить created_by"""
        # Устанавливаем created_by на основе текущего пользователя
        employer = Employer.objects.get(email=self.request.user.email)
        serializer.save(created_by=employer)  # Устанавливаем создателя вакансии

    def put(self, request, *args, **kwargs):
        """Используем встроенную логику put"""
        return super().put(request, *args, **kwargs)
    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#API для резюме
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class UserResumeListView(generics.ListAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Получаем текущего пользователя из запроса
        user = self.request.user
        print("Текущий пользователь:", self.request.user)
        # Проверяем, является ли пользователь экземпляром `Applicant`
        if not hasattr(user, 'applicant'):
            raise PermissionDenied("Только пользователи-аппликанты могут просматривать резюме.")
        
        # Фильтруем резюме по текущему пользователю
        return Resume.objects.filter(applicant=user)
    
class UserResumeDetailView(generics.RetrieveAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Получаем текущего пользователя
        user = self.request.user
        # Проверяем, является ли пользователь аппликантом
        if not hasattr(user, 'applicant'):
            raise PermissionDenied("Только пользователи-аппликанты могут просматривать резюме.")
        
        # Фильтруем резюме по текущему пользователю
        return Resume.objects.filter(applicant=user)
    

class UserResumeCreateView(generics.CreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            # Проверка, что пользователь является экземпляром Applicant
            applicant = Applicant.objects.get(email=self.request.user.email)
            serializer.save(applicant=applicant)
        except ObjectDoesNotExist:
            raise ValidationError("Только соискатели могут создавать резюме.")