# Generated by Django 5.1.3 on 2024-11-19 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0018_resume_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="vacancy",
            name="languages",
            field=models.ManyToManyField(
                blank=True, to="api.language", verbose_name="Языки"
            ),
        ),
    ]
