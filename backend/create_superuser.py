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
except ImproperlyConfigured:
    print("Не удалось найти модель пользователя. Проверьте AUTH_USER_MODEL в settings.py")
employer_email = 'employer12345@example.com'
employer_password = 'Buch555789'  # Конкретный пароль для работодателя
employer = Employer.objects.create(
    email=employer_email,
    password=employer_password,  # Устанавливаем конкретный пароль
    company_name='Example Company',
    company_info='Some information about the company'
)
employer.save()

# Создаем пользователя Applicant
applicant_email = 'applicant12345@example.com'
applicant_password = 'Buch555789'  # Конкретный пароль для соискателя
applicant = Applicant.objects.create(
    email=applicant_email,
    password=applicant_password,  # Устанавливаем конкретный пароль
    first_name='John',
    last_name='Doe',
    patronymic='Ivanovich'
)
applicant.save()

print("Employer and Applicant have been added to the database.")
