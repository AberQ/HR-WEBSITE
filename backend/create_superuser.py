import os
import django
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()
from registration.models import Employer, Applicant
# Получаем модель пользователя
User = get_user_model()

try:
    # Проверяем, существует ли суперпользователь с заданным email
    if not User.objects.filter(email='egor.master2017@gmail.com').exists():
        User.objects.create_superuser(
            email='egor.master2017@gmail.com',
            password='1'
        )
        print("Superuser created!")
    else:
        print("Superuser already exists.")
    
    # Проверяем, существует ли уже работодатель с таким email
    if not Employer.objects.filter(email='employer12345@example.com').exists():
        # Создаем работодателя (Employer)
        employer_email = 'employer123456@example.com'
        employer_password = 'Buch555789'
        employer = Employer.objects.create(
            email=employer_email,
            password=employer_password,
            company_name='Example Company',
            company_info='Some information about the company'
        )
        employer.save()
        print("Employer created!")
    else:
        print("Employer with this email already exists.")
    
    # Проверяем, существует ли уже соискатель с таким email
    if not Applicant.objects.filter(email='applicant12345@example.com').exists():
        # Создаем соискателя (Applicant)
        applicant_email = 'applicant123456@example.com'
        applicant_password = 'Buch555789'
        applicant = Applicant.objects.create(
            email=applicant_email,
            password=applicant_password,
            first_name='John',
            last_name='Doe',
            patronymic='Ivanovich'
        )
        applicant.save()
        print("Applicant created!")
    else:
        print("Applicant with this email already exists.")
    
except ImproperlyConfigured:
    print("Не удалось найти модель пользователя. Проверьте AUTH_USER_MODEL в settings.py")
except Exception as e:
    print(f"Произошла ошибка: {e}")