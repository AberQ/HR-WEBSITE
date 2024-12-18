# Generated by Django 4.2.6 on 2024-11-07 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0010_alter_language_options_remove_resume_created_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resume",
            name="degree",
            field=models.CharField(
                choices=[
                    ("speciality", "Специалитет"),
                    ("bachelor", "Бакалавриат"),
                    ("unfinished_higher", "Неоконченное высшее"),
                    ("vocational", "СПО"),
                ],
                max_length=100,
                verbose_name="Степень",
            ),
        ),
    ]
