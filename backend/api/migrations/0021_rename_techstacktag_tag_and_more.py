# Generated by Django 5.1.3 on 2024-11-24 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0020_remove_resume_work_experience_resume_experience"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="TechStackTag",
            new_name="Tag",
        ),
        migrations.RenameField(
            model_name="resume",
            old_name="tech_stack_tags",
            new_name="tags",
        ),
        migrations.RenameField(
            model_name="vacancy",
            old_name="tech_stack_tags",
            new_name="tags",
        ),
    ]
