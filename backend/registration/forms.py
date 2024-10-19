from django import forms
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        
class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(label="Email")  # Добавьте это поле
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser  # Используйте вашу модель пользователя
        fields = ('email', 'password')  # Убедитесь, что используете email для входа