import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()
#Эта строчка ПРИНЦИПИАЛЬНО ДОЛЖНА БЫТЬ НИЖЕ django.setup()
from registration.models import Employer, Applicant

# Создаем пользователя Employer
employer_email = 'employer123@example.com'
employer_password = 'Buch555789'  # Конкретный пароль для работодателя
employer = Employer.objects.create(
    email=employer_email,
    password=employer_password,  # Устанавливаем конкретный пароль
    company_name='Example Company',
    company_info='Some information about the company'
)
employer.save()

# Создаем пользователя Applicant
applicant_email = 'applicant123@example.com'
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
