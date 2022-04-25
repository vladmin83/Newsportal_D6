from django import forms
from django.forms import ModelForm, BooleanField
from .models import New, User, CategoryToUser


# Создаём модельную форму
class NewForm(ModelForm):
    check_box = BooleanField(label='Ало, Галочка!')
    # в класс мета, как обычно, надо написать модель, по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = New
        fields = ['title', 'categoryType', 'newCategory', 'text', 'author', 'check_box']


class UserForm(ModelForm):
    username = forms.CharField(label='Логин', max_length=32)
    first_name = forms.CharField(label='Имя', max_length=32)
    last_name = forms.CharField(label='Фамилия', max_length=32)
    email = forms.EmailField(label='"Электронная почта')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


# class SubscribeForm(ModelForm):
#     user = forms.ChoiceField(queryset=User.objects.all, label='Пользователь')
#     category = forms.ChoiceField(queryset=Category.objects.all, label='Категории')
#
#     class Meta:
#         model = CategoryToUser
#         fields = ['user', 'category']

