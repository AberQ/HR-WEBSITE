from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .models import *
class SignUpForm(UserCreationForm):
    class Meta:
        model = Applicant
        fields = ('email', 'first_name', 'last_name', 'patronymic', 'password1', 'password2')


CustomUser = get_user_model()

class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )



    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        # Проверяем, существует ли пользователь с данным email
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("Неверный email или пароль")

        # Проверка пароля
        if not user.check_password(password):
            raise forms.ValidationError("Неверный email или пароль")

        self.user_cache = user
        return self.cleaned_data
    
from django import forms
from api.models import Vacancy
from django_select2.forms import Select2MultipleWidget
class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = [
            'title',
            'work_format',
            'min_salary',
            'max_salary',
            'currency',
            'experience',
            'city',
            'address',
            'number_of_openings',
            'description',
            'tech_stack_tags',
            'work_condition_tags',
        ]
        widgets = {
            'tech_stack_tags': Select2MultipleWidget,  # Подключаем Select2 для tech_stack_tags
        }