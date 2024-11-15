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
    tech_stack_tags_list = [
    'JavaScript', 'HTML/CSS', 'React', 'Node.js', 'Angular', 'Vue.js', 'TypeScript', 
    'Swift', 'Kotlin', 'C#', '.NET', 'Ruby on Rails', 'PHP', 'MySQL', 'PostgreSQL', 
    'MongoDB', 'AWS', 'Azure', 'Google Cloud Platform', 'DevOps', 'Docker', 
    'Kubernetes', 'Jenkins', 'Git', 'GitHub Actions', 'API Design', 'RESTful API', 
    'GraphQL', 'Django', 'Flask', 'FastAPI', 'TensorFlow', 'PyTorch', 'Machine Learning', 
    'Data Analysis', 'Big Data', 'Hadoop', 'Spark', 'Cybersecurity', 'Penetration Testing', 
    'Ethical Hacking', 'Blockchain', 'Smart Contracts', 'IoT (Internet of Things)', 
    'SQL Optimization', 'Web Scraping', 'UX/UI Design', 'Figma', 'Adobe XD', 'AR/VR Development', 
    'Бариста', 'Официант', 'Горничная', 'Администратор гостиницы', 'Приготовление коктейлей', 
    'Уборка помещений', 'Сервировка стола', 'Работа с клиентами', 'Консультация по меню', 
    'Прием заказов', 'Работа с POS-терминалами', 'Знание санитарных норм', 
    'Устранение конфликтных ситуаций', 'Организация мероприятий', 'Навыки хостес', 
    'Проведение инвентаризации', 'Работа с кассой', 'Навыки ведения учета', 'Знание ассортимента', 
    'Подготовка к банкетам', 'Ответственность', 'Трудолюбие', 'Пунктуальность', 'Эмпатия', 
    'Коммуникабельность', 'Стрессоустойчивость', 'Умение работать в команде', 
    'Лидерские качества', 'Самоорганизация', 'Гибкость', 'Креативность', 
    'Навыки решения проблем', 'Дисциплина', 'Целеустремленность', 'Тайм-менеджмент', 
    'Обучаемость', 'Внимательность к деталям', 'Презентабельность', 'Уверенность в себе', 
    'Проактивность', 'Холодные звонки', 'Работа с возражениями', 'CRM-системы', 
    'Проведение переговоров', 'Прямые продажи', 'Анализ рынка', 'Формирование КП', 
    'Заключение сделок', 'Продажа услуг', 'Продажа B2B', 'Продажа B2C', 'Навыки презентации', 
    'Составление скриптов продаж', 'Управление продажами', 'Планирование продаж', 
    'Консультирование клиентов', 'Презентация товара', 'Мерчендайзинг', 'Поиск клиентов', 
    'Ведение отчетности', 'Вождение автомобиля', 'Категория A', 'Категория B', 
    'Категория C', 'Категория D', 'Управление спецтехникой', 'Логистика', 'Доставка грузов', 
    'Упаковка грузов', 'Работа с GPS', 'Навыки механика', 'Обслуживание автомобилей', 
    'Технический осмотр', 'Замена масел', 'Шиномонтаж', 'Работа с автопарком', 'Навигация', 
    'Ведение маршрутов', 'Навыки грузоперевозок', 'Безопасное вождение', 'Управление проектами', 
    'Организация встреч', 'Делопроизводство', 'Маркетинг', 'SEO', 'SMM', 'Работа с Google Analytics', 
    'Копирайтинг', 'Редактирование текстов', 'Переводы', 'Бухгалтерия', 'Финансовый анализ', 
    'Работа с Excel', 'Ведение переговоров', 'Обучение персонала', 'Работа с детьми', 
    'Ремонт бытовой техники', 'Электромонтаж', 'Сантехника', 'Малярные работы', 
    'Работа с чертежами', 'Навыки дизайна интерьеров', 'Организация логистики', 'Работа в 1С', 
    'Разработка презентаций', 'Актерское мастерство', 'Навыки оратора', 'Фотография', 
    'Видеомонтаж', 'Управление дроном', 'Наставничество', 'Навыки делового общения', 
    'Умение вести дебаты', 'Навыки убеждения', 'Решение конфликтов', 'Этикет', 'Грамотность', 
    'Умение мотивировать', 'Навыки дипломатии', 'Честность', 'Оптимизм', 'Самоконтроль', 
    'Логическое мышление', 'Позитивное мышление', 'Харизма', 'Ориентация на результат', 
    'Ориентация на клиента', 'Саморазвитие', 'Интуиция', 'Чувство юмора', 'Python', 'Дружелюбность',
]
    for tag_name in tech_stack_tags_list:
        if not TechStackTag.objects.filter(name=tag_name).exists():
            tag = TechStackTag(name=tag_name)
            tag.save()
            #print(f"TechStackTag '{tag_name}' created!")
        #else:
            #print(f"TechStackTag '{tag_name}' already exists.")
    print("Навыки готовы")
    
    # Добавляем Languages
    languages = [
    'Русский', 'Английский', 'Арабский', 'Китайский',
    'Испанский', 'Французский', 'Хинди', 'Бенгальский', 'Португальский', 'Индонезийский',
    'Японский', 'Немецкий', 'Корейский', 'Вьетнамский', 'Тамильский', 'Турецкий', 'Итальянский',
    'Польский', 'Украинский', 'Малайский', 'Персидский', 'Тагальский', 'Нидерландский', 'Тайский',
    'Греческий', 'Чешский', 'Румынский', 'Шведский', 'Иврит', 'Датский'
]
    for language_name in languages:
        if not Language.objects.filter(name=language_name).exists():
            language = Language(name=language_name)
            language.save()
            #print(f"Language '{language_name}' created!")
        #else:
            #print(f"Language '{language_name}' already exists.")
    print("Языки готовы")
    
    # Создаем Vacancy, ссылаясь на созданного работодателя
    if employer:
        if not Vacancy.objects.filter(title='Junior Python Developer', created_by=employer).exists():
            vacancy = Vacancy(
                title='Junior Python Developer',
                created_by=employer,  # Замените employer на корректное поле, если оно отличается
                min_salary=50000,
                max_salary=70000,
                currency='RUB',
                experience='До 1 года',
                number_of_openings = 1,
                city='Москва',
                address='Улица фронтендеров, 69',
                description='Описание вакансии для теста.',
                status='Published'
            )
            vacancy.save()
            # Присвоение навыков к вакансии
            tech_stack_tags_list = TechStackTag.objects.filter(name__in=['Python', 'Дружелюбность'])
            vacancy.tech_stack_tags.set(tech_stack_tags_list)
            print(f"Vacancy 'Junior Python Developer' created!")
        else:
            print(f"Vacancy 'Junior Python Developer' already exists.")
    
    # Создаем Resume, ссылаясь на созданного соискателя
    if applicant:
        resume_candidate_name = 'Тест Тестов'
        if not Resume.objects.filter(candidate_name=resume_candidate_name).exists():
            resume = Resume(
                desired_position='Junior Python Developer',
                candidate_name=resume_candidate_name,
                email=applicant_email,
                phone='+7 123 456 7890',
                city='Москва',
                specialization='Программирование',
                degree='bachelor',  # Пример степени
                work_experience='1',  # Пример опыта в годах
                
                portfolio_link='https://github.com/AberQ/HR-WEBSITE',  # Пример пустой ссылки на портфолио
                applicant=applicant  # Ссылаемся на Applicant
            )
            resume.save()
            #Присвоение тэгов и языков к резюме
            tech_stack_tags_list = TechStackTag.objects.filter(name__in=['Python', 'Дружелюбность'])
            languages = Language.objects.filter(name__in=['Русский', 'Английский'])
            resume.tech_stack_tags.set(tech_stack_tags_list)
            resume.languages.set(languages)
            print(f"Resume for {resume_candidate_name} created!")
        else:
            resume = Resume.objects.get(candidate_name=resume_candidate_name)
            print(f"Resume for {resume_candidate_name} already exists.")
    

except ImproperlyConfigured:
    print("Не удалось найти модель пользователя. Проверьте AUTH_USER_MODEL в settings.py")
except Exception as e:
    print(f"Произошла ошибка: {e}")
