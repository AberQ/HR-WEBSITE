from django.contrib import admin
from api.models import *
from django.core.exceptions import ValidationError

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'min_salary', 'max_salary', 'currency', 'experience', 'number_of_openings', 'publication_date', 'status', 'work_format', 'work_condition_tags')
    search_fields = ('title', 'city', 'description')
    list_filter = ('currency', 'city', 'experience', 'publication_date', 'status', 'work_format', 'work_condition_tags')
    filter_horizontal = ('tech_stack_tags',)  # Оставляем только для tech_stack_tags

    # Добавление пользовательского сообщения при ошибке валидации
    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()  # Проверка на валидацию перед сохранением
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            form.add_error('number_of_openings', e.messages)

# Так как поле work_condition_tags больше не ManyToMany, удаляем его из админки
@admin.register(TechStackTag)
class TechStackTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)



class ResumeAdmin(admin.ModelAdmin):
    list_display = ('candidate_name', 'desired_position', 'email', 'phone', 'city', 'created_at')  # Поля, которые будут отображаться в списке
    search_fields = ('candidate_name', 'email', 'desired_position')  # Поля, по которым будет осуществляться поиск
    list_filter = ('city', 'degree', 'graduation_year')  # Фильтры для списка
    ordering = ('-created_at',)  # Сортировка по дате создания по убыванию

admin.site.register(Resume, ResumeAdmin)  # Регистрация модели Resume с указанным админ-классом