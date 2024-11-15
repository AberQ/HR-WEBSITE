#!/bin/bash

# Применяем миграции
echo "Checking migrations..."
python manage.py makemigrations
echo "Applying migrations..."
python manage.py migrate

echo 'Insert test data...'
python add_test_data.py

# Запускаем сервер
echo "Starting the server..."
python manage.py runserver 0.0.0.0:8000
