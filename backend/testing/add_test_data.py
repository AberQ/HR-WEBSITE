import os
import sys
import django
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.core.cache import cache

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")
django.setup()

from api.models import Language, Resume, Tag, Vacancy
from registration.models import Applicant, Employer
from testing.test_data import *

# Получаем модель пользователя
User = get_user_model()

# Входные данные
admin_email = "admin@example.com"
admin_password = "1"

employer_email = "employer@example.com"
employer_password = "1"

applicant_email = "applicant@example.com"
applicant_password = "1"

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
        employer = Employer(
            email=employer_email,
            company_name="Example Company",
            company_info="Some information about the company",
        )
        employer.set_password(employer_password)
        employer.save()
        print(f"Employer {employer_email} created!")
    else:
        employer = Employer.objects.get(email=employer_email)
        print(f"Employer with {employer_email} already exists.")

    # Проверяем и создаем соискателя
    if not Applicant.objects.filter(email=applicant_email).exists():
        applicant = Applicant(
            email=applicant_email,
            first_name="John",
            last_name="Doe",
            patronymic="Ivanovich",
        )
        applicant.set_password(applicant_password)
        applicant.save()
        print(f"Applicant {applicant_email} created!")
    else:
        applicant = Applicant.objects.get(email=applicant_email)
        print(f"Applicant with {applicant_email} already exists.")

    # Добавляем TechStackTags и кешируем их в Redis
    for tag_name in tags_list:
        tag = cache.get(tag_name)
        if not tag:
            if not Tag.objects.filter(name=tag_name).exists():
                tag = Tag(name=tag_name)
                tag.save()
                cache.set(tag_name, tag)
                print(f"Tag '{tag_name}' created and cached!")
            else:
                tag = Tag.objects.get(name=tag_name)
                cache.set(tag_name, tag)
                print(f"Tag '{tag_name}' already exists and cached.")
        else:
            print(f"Tag '{tag_name}' found in cache.")

    print("Навыки готовы")

    # Добавляем Languages и кешируем их в Redis
    for language_name in languages:
        language = cache.get(language_name)
        if not language:
            if not Language.objects.filter(name=language_name).exists():
                language = Language(name=language_name)
                language.save()
                cache.set(language_name, language)
                print(f"Language '{language_name}' created and cached!")
            else:
                language = Language.objects.get(name=language_name)
                cache.set(language_name, language)
                print(f"Language '{language_name}' already exists and cached.")
        else:
            print(f"Language '{language_name}' found in cache.")

    print("Языки готовы")

    # Создаем Vacancy, ссылаясь на созданного работодателя
    if employer:
        if not Vacancy.objects.filter(
            title="Junior Python Developer", created_by=employer
        ).exists():
            vacancy = Vacancy(
                title="Junior Python Developer",
                created_by=employer,
                min_salary=50000,
                max_salary=70000,
                currency="RUB",
                experience="До 1 года",
                number_of_openings=1,
                city="Москва",
                address="Улица фронтендеров, 69",
                description="Описание вакансии для теста.",
                status="Published",
            )
            vacancy.save()
            # Присвоение навыков к вакансии
            tags_list = Tag.objects.filter(name__in=["Python", "Дружелюбность"])
            vacancy.tags.set(tags_list)
            languages = Language.objects.filter(name__in=["Русский", "Английский"])
            vacancy.languages.set(languages)
            print(f"Vacancy 'Junior Python Developer' created!")
        else:
            print(f"Vacancy 'Junior Python Developer' already exists.")

    # Создаем Resume, ссылаясь на созданного соискателя
    if applicant:
        resume_candidate_name = "Тест Тестов"
        if not Resume.objects.filter(candidate_name=resume_candidate_name).exists():
            resume = Resume(
                desired_position="Junior Python Developer",
                candidate_name=resume_candidate_name,
                email=applicant_email,
                content="Контент",
                phone="+7 123 456 7890",
                city="Москва",
                experience="До 1 года",
                specialization="Программирование",
                degree="bachelor",
                portfolio_link="https://github.com/AberQ/HR-WEBSITE",
                applicant=applicant,
            )
            resume.save()
            # Присвоение тэгов и языков к резюме
            tags_list = Tag.objects.filter(name__in=["Python", "Дружелюбность"])
            languages = Language.objects.filter(name__in=["Русский", "Английский"])
            resume.tags.set(tags_list)
            resume.languages.set(languages)
            print(f"Resume for {resume_candidate_name} created!")
        else:
            resume = Resume.objects.filter(candidate_name=resume_candidate_name)
            print(f"Resume for {resume_candidate_name} already exists.")

except ImproperlyConfigured:
    print("Не удалось найти модель пользователя. Проверьте AUTH_USER_MODEL в settings.py")
except Exception as e:
    print(f"Произошла ошибка: {e}")
