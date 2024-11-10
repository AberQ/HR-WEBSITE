#!/bin/bash

# Применяем миграции
echo "Applying migrations..."
python manage.py migrate


# Запускаем сервер
echo "Starting the server..."
python manage.py runserver 0.0.0.0:8000
