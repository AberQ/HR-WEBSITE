import os
import django
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()
from registration.models import Employer, Applicant

# Получаем модель пользователя
User = get_user_model()

# Входные данные
admin_email = 'admin@example.com'
admin_password = '1'

employer_email = 'employer@example.com'
employer_password = '1'

applicant_email = 'applicant@example.com'
applicant_password = '1'

try:
    # Проверяем, существует ли суперпользователь с заданным email
    if not User.objects.filter(email=admin_email).exists():
        admin_user = User(email=admin_email)
        admin_user.set_password(admin_password)  # Хешируем пароль
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.save()
        print(f"Superuser {admin_email} created!")
    else:
        print(f"Superuser {admin_email} already exists.")
    
    # Проверяем, существует ли уже работодатель с таким email
    if not Employer.objects.filter(email=employer_email).exists():
        employer = Employer(email=employer_email, company_name='Example Company', company_info='Some information about the company')
        employer.set_password(employer_password)  # Хешируем пароль
        employer.save()
        print(f"Employer {employer_email} created!")
    else:
        print(f"Employer with {employer_email} already exists.")
    
    # Проверяем, существует ли уже соискатель с таким email
    if not Applicant.objects.filter(email=applicant_email).exists():
        applicant = Applicant(email=applicant_email, first_name='John', last_name='Doe', patronymic='Ivanovich')
        applicant.set_password(applicant_password)  # Хешируем пароль
        applicant.save()
        print(f"Applicant {applicant_email} created!")
    else:
        print(f"Applicant with {applicant_email} already exists.")
    
except ImproperlyConfigured:
    print("Не удалось найти модель пользователя. Проверьте AUTH_USER_MODEL в settings.py")
except Exception as e:
    print(f"Произошла ошибка: {e}")
