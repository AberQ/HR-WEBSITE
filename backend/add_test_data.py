import os
import django
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()

from registration.models import Employer, Applicant
from api.models import TechStackTag, Language, Vacancy, Resume

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
    # Проверяем и создаем суперпользователя
    if not User.objects.filter(email=admin_email).exists():
        admin_user = User(email=admin_email)
        admin_user.set_password(admin_password)
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.save()
        print(f"Superuser {admin_email} created!")
    else:
        print(f"Superuser {admin_email} already exists.")
    
    # Проверяем и создаем работодателя
    if not Employer.objects.filter(email=employer_email).exists():
        employer = Employer(email=employer_email, company_name='Example Company', company_info='Some information about the company')
        employer.set_password(employer_password)
        employer.save()
        print(f"Employer {employer_email} created!")
    else:
        employer = Employer.objects.get(email=employer_email)
        print(f"Employer with {employer_email} already exists.")
    
    # Проверяем и создаем соискателя
    if not Applicant.objects.filter(email=applicant_email).exists():
        applicant = Applicant(email=applicant_email, first_name='John', last_name='Doe', patronymic='Ivanovich')
        applicant.set_password(applicant_password)
        applicant.save()
        print(f"Applicant {applicant_email} created!")
    else:
        applicant = Applicant.objects.get(email=applicant_email)
        print(f"Applicant with {applicant_email} already exists.")
    
    # Добавляем TechStackTags
    tech_stack_tags = ['Python', 'Дружелюбность']
    for tag_name in tech_stack_tags:
        if not TechStackTag.objects.filter(name=tag_name).exists():
            tag = TechStackTag(name=tag_name)
            tag.save()
            print(f"TechStackTag '{tag_name}' created!")
        else:
            print(f"TechStackTag '{tag_name}' already exists.")
    
    # Добавляем Languages
    languages = ['Русский', 'Английский']
    for language_name in languages:
        if not Language.objects.filter(name=language_name).exists():
            language = Language(name=language_name)
            language.save()
            print(f"Language '{language_name}' created!")
        else:
            print(f"Language '{language_name}' already exists.")
    

except ImproperlyConfigured:
    print("Не удалось найти модель пользователя. Проверьте AUTH_USER_MODEL в settings.py")
except Exception as e:
    print(f"Произошла ошибка: {e}")
