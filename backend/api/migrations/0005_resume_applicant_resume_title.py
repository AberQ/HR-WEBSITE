# Generated by Django 4.2.6 on 2024-11-03 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0008_alter_employer_company_name'),
        ('api', '0004_resume'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='applicant',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='applicant_resumes', to='registration.applicant'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resume',
            name='title',
            field=models.CharField(blank=True, max_length=255, verbose_name='Заголовок резюме'),
        ),
    ]
