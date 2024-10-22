# Generated by Django 4.2.6 on 2024-10-18 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_vacancy_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='status',
            field=models.CharField(choices=[('published', 'Опубликована'), ('archived', 'В архиве'), ('checking', 'На проверке')], default='published', max_length=10),
        ),
    ]