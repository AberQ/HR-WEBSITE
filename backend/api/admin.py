from django.contrib import admin
from api.models import *
from django.core.exceptions import ValidationError

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'min_salary', 'max_salary', 'currency', 'experience', 'number_of_openings', 'publication_date', 'status', 'format', 'employment_type')
    search_fields = ('title', 'city', 'description')
    list_filter = ('currency', 'city', 'experience', 'publication_date', 'status', 'format', 'employment_type')
    filter_horizontal = ('tech_stack_tags',)  # Оставляем только для tech_stack_tags

    # Добавление пользовательского сообщения при ошибке валидации
    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()  # Проверка на валидацию перед сохранением
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            form.add_error('number_of_openings', e.messages)

# Так как поле employment_type больше не ManyToMany, удаляем его из админки
@admin.register(TechStackTag)
class TechStackTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)



class ResumeAdmin(admin.ModelAdmin):
    list_display = ('candidate_name', 'desired_position', 'email', 'phone', 'city', 'updated_at')  # Поля, которые будут отображаться в списке
    search_fields = ('candidate_name', 'email', 'desired_position')  # Поля, по которым будет осуществляться поиск
    list_filter = ('city',)  # Фильтры для списка
    ordering = ('-updated_at',)  # Сортировка по дате создания по убыванию
    filter_horizontal = ('languages', 'tech_stack_tags')  # Оставляем только для tech_stack_tags

admin.site.register(Resume, ResumeAdmin)  # Регистрация модели Resume с указанным админ-классом


class LanguageAdmin(admin.ModelAdmin):
    list_display = ( 'name',)  # Поля, которые будут отображаться в списке
    search_fields = ('name',)  # Поля, по которым будет осуществляться поиск

# Регистрация моделей в админке
admin.site.register(Language, LanguageAdmin)
