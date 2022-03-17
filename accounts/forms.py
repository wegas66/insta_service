from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class LoginForm(forms.Form):
    """Форма для входа"""

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': "email", "class": 'input', "id": "user2"})
    )
    password = forms.CharField(
        max_length=150,
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': "Пароль*", "class": 'input', "id": "password"})
    )


class SignUpForm(UserCreationForm):
    """Форма для регистрации"""

    password1 = forms.CharField(
        label='Пароль',
        max_length=300,
        widget=forms.PasswordInput(attrs={'placeholder': "Пароль", "class": "input", "id": "password1"})
    )
    password2 = forms.CharField(
        label='Пароль ещё раз',
        max_length=300,
        widget=forms.PasswordInput(attrs={'placeholder': "Пароль ещё раз", "class": "input", "id": "password2"})
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': "Email*", "class": "input", "id": "email2"}),
        }


class UserUpdateForm(forms.ModelForm):
    """Форма для обновления профиля юзера"""

    password1 = forms.CharField(
        label='',
        max_length=300,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        required=False
    )
    password2 = forms.CharField(
        label='',
        max_length=300,
        widget=forms.PasswordInput(attrs={"autocomplete": "false"}),
        required=False
    )

    class Meta:
        model = User
        fields = ('password1', 'password2')
