# Generated by Django 4.2.6 on 2024-10-31 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("registration", "0007_alter_applicant_first_name_alter_applicant_last_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employer",
            name="company_name",
            field=models.CharField(max_length=255, verbose_name="Имя компании"),
        ),
    ]
