# Generated by Django 4.2.6 on 2024-11-03 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_alter_vacancy_created_by"),
    ]

    operations = [
        migrations.CreateModel(
            name="Resume",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "candidate_name",
                    models.CharField(max_length=255, verbose_name="Имя кандидата"),
                ),
                ("email", models.EmailField(max_length=254, verbose_name="Email")),
                ("phone", models.CharField(max_length=20, verbose_name="Телефон")),
                ("city", models.CharField(max_length=255, verbose_name="Город")),
                (
                    "desired_position",
                    models.CharField(max_length=255, verbose_name="Желаемая должность"),
                ),
                (
                    "education_institution",
                    models.CharField(max_length=255, verbose_name="Учебное заведение"),
                ),
                ("degree", models.CharField(max_length=100, verbose_name="Степень")),
                (
                    "graduation_year",
                    models.PositiveIntegerField(verbose_name="Год выпуска"),
                ),
                ("work_experience", models.TextField(verbose_name="Опыт работы")),
                (
                    "languages",
                    models.CharField(blank=True, max_length=255, verbose_name="Языки"),
                ),
                (
                    "portfolio_link",
                    models.URLField(blank=True, verbose_name="Ссылка на портфолио"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Дата обновления"),
                ),
                (
                    "skills",
                    models.ManyToManyField(
                        blank=True, to="api.techstacktag", verbose_name="Навыки"
                    ),
                ),
            ],
            options={
                "verbose_name": "Резюме",
                "verbose_name_plural": "Резюме",
            },
        ),
    ]
