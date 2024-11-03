# Generated by Django 4.2.6 on 2024-11-03 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_resume_languages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Язык')),
            ],
        ),
        migrations.RemoveField(
            model_name='resume',
            name='languages',
        ),
        migrations.AddField(
            model_name='resume',
            name='languages',
            field=models.ManyToManyField(blank=True, to='api.language', verbose_name='Языки'),
        ),
    ]
