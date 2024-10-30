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
