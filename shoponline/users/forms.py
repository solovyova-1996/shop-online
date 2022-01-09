import hashlib
from random import random

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, \
    UserChangeForm
from django import forms
from django.core.exceptions import ValidationError

from users.models import User


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        # добавляем стили для полей формы
        self.fields['username'].widget.attrs[
            'placeholder'] = 'Введите имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1',
                  'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        # добавляем стили для полей формы
        self.fields['username'].widget.attrs[
            'placeholder'] = 'Введите имя пользователя'
        self.fields['email'].widget.attrs[
            'placeholder'] = 'Введите адрес эл. почты'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя '
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs[
            'placeholder'] = 'Подтвердите пароль'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if email:
    #         raise ValidationError('Такая почта уже зарегистрирована')
    #     return email
    # переопределяем метод сохранения, чтобы пользователь проходил верификацию по почте
    def save(self, commit=True):
        user = super(UserRegisterForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random()).encode('utf-8')).hexdigest()[:6]
        # создаем ключ для активации и добавляем в него соль
        user.activation_key = hashlib.sha1(
            (user.email + salt).encode('utf-8')).hexdigest()
        user.save()
        return user

class UserProfileForm(UserChangeForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'image', 'age')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # поля только для чтения
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'

    #  недопускается добавление файлов большего размера  # def clean_image(self):  #     data = self.cleaned_data['image']  #     if data.size > 1024:  #         raise forms.ValidationError('Файл слишком большой')  #     return data
