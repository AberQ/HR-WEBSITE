# Generated by Django 5.1.3 on 2024-11-14 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_rename_work_condition_tags_vacancy_employment_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resume',
            old_name='skills',
            new_name='tech_stack_tags',
        ),
    ]