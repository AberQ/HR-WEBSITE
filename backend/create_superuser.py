#Этот файл нужен для автоматического создания пользователей, вакансий и резюме для тестирования
import os
import django
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()
from registration.models import Employer, Applicant
# Получаем модель пользователя
User = get_user_model()


#Входные данные
admin_email = 'admin@example.com'
admin_password = 'Test555789'

employer_email = 'employer@example.com'
employer_password = 'Test555789'

applicant_email = 'applicant@example.com'
applicant_password = 'Test555789'

try:
    # Проверяем, существует ли суперпользователь с заданным email
    if not User.objects.filter(email=admin_email).exists():
        User.objects.create_superuser(
            email=admin_email,
            password=admin_password
        )
        print(f"Superuser {admin_email} created!")
    else:
        print(f"Superuser {admin_email} already exists.")
    
    # Проверяем, существует ли уже работодатель с таким email
    if not Employer.objects.filter(email=employer_email).exists():
        # Создаем работодателя (Employer)
        
        employer = Employer.objects.create(
            email=employer_email,
            password=employer_password,
            company_name='Example Company',
            company_info='Some information about the company'
        )
        employer.save()
        print(f"Employer {employer_email} created!")
    else:
        print(f"Employer with {employer_email} already exists.")
    
    # Проверяем, существует ли уже соискатель с таким email
    if not Applicant.objects.filter(email=applicant_email).exists():
        # Создаем соискателя (Applicant)
        
        applicant = Applicant.objects.create(
            email=applicant_email,
            password=applicant_password,
            first_name='John',
            last_name='Doe',
            patronymic='Ivanovich'
        )
        applicant.save()
        print(f"Applicant {applicant_email} created!")
    else:
        print(f"fApplicant with {applicant_email} already exists.")
    
except ImproperlyConfigured:
    print("Не удалось найти модель пользователя. Проверьте AUTH_USER_MODEL в settings.py")
except Exception as e:
    print(f"Произошла ошибка: {e}")