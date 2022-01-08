from django import forms

from mainapp.models import Category
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserAdminRegisterForm(UserRegisterForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1',
                  'password2', 'image')

    def __init__(self, *args, **kwargs):
        super(UserAdminRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs['class'] = 'form-control '


class UserAdminProfileForm(UserProfileForm):

    def __init__(self, *args, **kwargs):
        super(UserAdminProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = False
        self.fields['email'].widget.attrs['readonly'] = False


class CategoryAdminCreate(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description',)

    def __init__(self, *args, **kwargs):
        super(CategoryAdminCreate, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs[
            'placeholder'] = 'Введите название категории'
        self.fields['description'].widget.attrs[
            'placeholder'] = 'Введите описание категории'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
