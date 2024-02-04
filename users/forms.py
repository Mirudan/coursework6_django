from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, \
    UserChangeForm

from users.models import User


class StyleFormMixin:
    """
   Обновление стилей форм восстановления пароля
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.ChoiceField):
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control mt-2 mb-2'


class HiddenPasswordMixin:
    """Скрытие пароля в форме"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    """
    Форма авторизации на сайте
    """
    pass


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Форма регистрации на сайте
    """

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserForgotPasswordForm(StyleFormMixin, PasswordResetForm):
    """
    Запрос на восстановление пароля
    """
    pass


class UserSetNewPasswordForm(StyleFormMixin, SetPasswordForm):
    """
    Изменение пароля пользователя после подтверждения
    """
    pass


class UserProfileForm(StyleFormMixin, HiddenPasswordMixin, UserChangeForm):
    """
     Форма обновления данных пользователя
     """

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)


class ModeratorUserForm(StyleFormMixin, HiddenPasswordMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('is_active',)
        labels = {
            'is_active': 'Не заблокирован',
        }


class AdminUserForm(StyleFormMixin, HiddenPasswordMixin, UserChangeForm):
    """
     Форма обновления данных пользователя
     """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_active')
