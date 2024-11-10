import os
import django
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()

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
