# Generated by Django 4.2.6 on 2024-10-31 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_alter_applicant_options_alter_employer_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='first_name',
            field=models.CharField(max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='last_name',
            field=models.CharField(max_length=150, verbose_name='last name'),
        ),
    ]
