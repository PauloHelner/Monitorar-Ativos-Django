from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.core import validators
from django.contrib.auth.password_validation import validate_password


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={"class": "email_field", "autofocus": True}),
    )
    password = forms.CharField(
        label="Senha", widget=forms.PasswordInput(attrs={"class": "pass_field"})
    )


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={"class": "email_field", "autofocus": True}),
    )
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "pass_field"}),
        validators=[validate_password],
    )
    password2 = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={"class": "pass_field"}),
    )

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")
