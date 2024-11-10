import os
import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()

# Получаем модель пользователя из настроек
try:
    User = settings.AUTH_USER_MODEL
    CustomUser = django.apps.apps.get_model(User)
except ImproperlyConfigured:
    raise ImproperlyConfigured("Не удалось найти модель пользователя. Проверьте AUTH_USER_MODEL в settings.py")

# Проверяем, существует ли суперпользователь с заданным email
if not CustomUser.objects.filter(email='egor.master2017@gmail.com').exists():
    CustomUser.objects.create_superuser(
        email='egor.master2017@gmail.com',
        password='1',
    )
    print("Superuser created!")
else:
    print("Superuser already exists.")
