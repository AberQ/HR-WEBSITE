from django.contrib import admin
from api.models import Vacancy, TechStackTag
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



from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from registration.models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    # Определите поля, которые будут отображаться в списке пользователей
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name')

    # Определите поля для формы редактирования
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личные данные', {'fields': ('first_name', 'last_name', 'patronymic')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )

    # Определите поля, которые будут отображаться в форме добавления
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active')}
        ),
    )

    # Укажите, какие поля могут быть редактируемыми
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

# Зарегистрируйте свой пользовательский класс в админ-панели
admin.site.register(CustomUser, CustomUserAdmin)
