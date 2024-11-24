from drf_yasg import openapi

properties_for_resume = {
    "desired_position": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="Желаемая должность кандидата",
        example="Junior Python Developer",
    ),
    "candidate_name": openapi.Schema(
        type=openapi.TYPE_STRING, description="ФИО кандидата", example="Тест Тестов"
    ),
    "content": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="Описание кандидата или сопроводительный текст",
        example="Меня зовут Тест, я увлекаюсь Python и создаю проекты на Django.",
    ),
    "contacts": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email", "phone"],
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_EMAIL,
                description="Email кандидата",
                example="applicant@example.com",
            ),
            "phone": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Телефон кандидата",
                example="+7 123 456 7890",
            ),
        },
        description="Контактная информация кандидата",
    ),
    "location": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["city"],
        properties={
            "city": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Город проживания кандидата",
                example="Москва",
            )
        },
        description="Местоположение кандидата",
    ),
    "degree": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="Уровень образования кандидата",
        example="bachelor",
    ),
    "skills": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "experience": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Количество лет опыта работы",
                example="1",
            ),
            "tags": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING),
                description="Технические навыки кандидата",
                example=["Python", "Дружелюбность"],
            ),
            "languages": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING),
                description="Языки, которыми владеет кандидат",
                example=["Русский", "Английский"],
            ),
        },
        description="Навыки кандидата",
    ),
    "portfolio_link": openapi.Schema(
        type=openapi.TYPE_STRING,
        format=openapi.FORMAT_URI,
        description="Ссылка на портфолио кандидата",
        example="https://github.com/AberQ/HR-WEBSITE",
    ),
}


properties_for_vacancies = {
    "title": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="Название вакансии. Например, 'Junior Python Developer'.",
        example="Junior Python Developer",
    ),
    "description": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="Описание вакансии.",
        example="Описание вакансии для теста.",
    ),
    "work_conditions": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description="Условия работы.",
        properties={
            "format": openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=["onsite", "remote", "hybrid"],
                description="Формат работы: на месте, удалённо или гибридный.",
                example="onsite",
            ),
            "employment_type": openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=[
                    "full_time",
                    "part_time",
                    "internship",
                    "volunteering",
                    "one_time",
                    "project",
                ],
                description="Тип занятости: полная ставка, частичная, стажировка и т.д.",
                example="full_time",
            ),
        },
    ),
    "salary": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description="Информация о зарплате.",
        properties={
            "min_salary": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="Минимальная зарплата.",
                example=50000,
            ),
            "max_salary": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="Максимальная зарплата.",
                example=70000,
            ),
            "currency": openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=["RUB", "USD", "EUR"],
                description="Валюта зарплаты, например, 'RUB'.",
                example="RUB",
            ),
        },
    ),
    "location": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description="Информация о месте работы.",
        properties={
            "city": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Город, где находится работа.",
                example="Москва",
            ),
            "address": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Адрес работы.",
                example="Улица фронтендеров, 69",
            ),
        },
    ),
    "number_of_openings": openapi.Schema(
        type=openapi.TYPE_INTEGER,
        description="Количество открытых позиций.",
        example=1,
    ),
    "skills": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description="Навыки и требования для кандидата.",
        properties={
            "experience": openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=["0", "1", "1-3", "3-6", "6"],
                description="""
                        Опыт работы кандидата
                        0 = Без опыта
                        1 = До 1 года
                        1-3 = от 1 до 3 лет
                        3-6 = от 3 до 6 лет
                        6 = более 6 лет
                        """,
                example="1",
            ),
            "tags": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING),
                description="Технический стек, требуемый для вакансии. Берутся из базы данных",
                example=["Python", "Дружелюбность"],
            ),
            "languages": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING),
                description="Языки, которыми должен владеть кандидат. Берутся из базы данных",
                example=["Русский", "Английский"],
            ),
        },
    ),
    "status": openapi.Schema(
        type=openapi.TYPE_STRING,
        enum=["published", "archived", "checking"],
        description="Статус вакансии: опубликована или архивирована или на проверке.",
        example="published",
    ),
}
