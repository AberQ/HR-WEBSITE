# Generated by Django 5.1.2 on 2024-10-18 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_vacancy_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='experience',
            field=models.CharField(choices=[('<1', 'До 1 года'), ('1-3', 'от 1 до 3 лет'), ('3-6', 'от 3 до 6 лет'), ('>6', 'более 6 лет')], default='<1', max_length=10),
        ),
    ]
