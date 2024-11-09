#!/bin/bash

# Применяем миграции
echo "Applying migrations..."
python manage.py migrate

# Создаем суперпользователя (если его нет)
echo "Creating superuser..."
python manage.py createsuperuser --noinput || echo "Superuser already exists."

# Запускаем сервер
echo "Starting the server..."
python manage.py runserver 0.0.0.0:8000
