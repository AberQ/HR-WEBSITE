from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from registration.models import *


class CustomUserAdmin(BaseUserAdmin):
    # Определите поля, которые будут отображаться в списке пользователей
    list_display = ('email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)
    search_fields = ('email',)

    # Определите поля для формы редактирования
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )

    # Определите поля, которые будут отображаться в форме добавления
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    # Укажите, какие поля могут быть редактируемыми
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

# Зарегистрируйте свой пользовательский класс в админ-панели
admin.site.register(CustomUser, CustomUserAdmin)


from django.contrib import admin

from .models import Employer  # Замените . на путь к вашей модели, если нужно


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'patronymic', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'date_joined')
    ordering = ('date_joined',)

    def save_model(self, request, obj, form, change):
        if not change:  # Если это новый объект
            obj.set_password(obj.password)  # Шифруем пароль перед сохранением
        super().save_model(request, obj, form, change)

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('email', 'company_name', 'company_info')
    search_fields = ('email', 'company_name')

    def save_model(self, request, obj, form, change):
        if not change:  # Если это новый объект
            obj.set_password(obj.password)  # Шифруем пароль перед сохранением
        super().save_model(request, obj, form, change)
