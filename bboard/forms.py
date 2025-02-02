from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import ModelForm, modelform_factory, Select, modelformset_factory
from django.forms.fields import DecimalField
from django.forms.models import BaseModelFormSet

from bboard.models import Bb, Rubric, Img, Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'phone_number']


class ImgForm(ModelForm):
    img = forms.ImageField(
        label='Изображение',
        # widget=forms.widgets.ClearableFileInput(attrs={'multiple': True}),
        validators=[validators.FileExtensionValidator(
            allowed_extensions=('gif', 'jpg', 'png'))],
        error_messages={
            'invalid_extension': 'Этот формат не поддерживается'})

    desc = forms.CharField(label='Описание',
                           widget=forms.widgets.Textarea())

    class Meta:
        model = Img
        fields = '__all__'


# Основной (вернуть)
class BbForm(ModelForm):
    title = forms.CharField(
        label='Название товара',
        validators=[validators.RegexValidator(regex='^.{4,}$')],
        error_messages={'invalid': 'Слишком короткое название товара'}
    )

    captcha = CaptchaField(label='Введите текст с картинки',
                           # generator='captcha.helpers.random_char_challenge',
                           # generator='captcha.helpers.math_challenge',
                           # generator='captcha.helpers.word_challenge',
                           error_messages={'invalid': 'Неправильный текст'})

    def clean_title(self):
        val = self.cleaned_data['title']
        if val == 'Прошлогодний снег':
            raise ValidationError('К продаже не допускается')
        return val

    def clean(self):
        super().clean()
        errors = {}
        if not self.cleaned_data['content']:
            errors['content'] = ValidationError(
                'Укажите описание продаваемого товара')
        if self.cleaned_data['price'] < 0:
            errors['price'] = ValidationError(
                'Укажите неотрицательное значение цены')

        if errors:
            raise ValidationError(errors)

    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric', 'img')
        help_texts = {'rubric': 'Не забудьте выбрать рубрику!'}


# Фабрика классов
# BbForm = modelform_factory(
#     Bb,
#     fields=('title', 'content', 'price', 'rubric'),
#     labels={'title': 'Название товара'},
#     help_texts={'rubric': 'Не забудьте выбрать рубрику!'},
#     field_classes={'price': DecimalField},
#     widgets={'rubric': Select(attrs={'size': 8})}
# )


# Быстрое объявление
# class BbForm(ModelForm):
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric')
#         labels = {'title': 'Название товара'}
#         help_texts = {'rubric': 'Не забудьте выбрать рубрику!'}
#         field_classes = {'price': DecimalField}
#         widgets = {'rubric': Select(attrs={'size': 8})}


# Полное объявление
# class BbForm(ModelForm):
#     title = forms.CharField(label='Название товара')
#     content = forms.CharField(label='Описание',
#                               widget=forms.widgets.Textarea())
#     price = forms.DecimalField(label='Цена', decimal_places=2)
#     rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
#                                     label='Рубрика',
#                                     help_text='Не забудьте выбрать рубрику!',
#                                     widget=forms.widgets.Select(attrs={'size': 8}))
#
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric')


# Полное объявление
# class BbForm(ModelForm):
#     price = forms.DecimalField(label='Цена', decimal_places=2)
#     rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
#                                     label='Рубрика',
#                                     help_text='Не забудьте выбрать рубрику!',
#                                     widget=forms.widgets.Select(attrs={'size': 8}))
#
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric')
#         labels = {'title': 'Название товара'}


class RegisterUserForm(ModelForm):
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Пароль (повторно)')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'last_name')


RubricFormSet = modelformset_factory(Rubric, fields=('name',),
                                     can_order=True, can_delete=True)


class RubricBaseFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()
        names = [form.cleaned_data['name'] for form in self.forms \
                 if 'name' in form.cleaned_data]
        if ('Недвижимость' not in names) or ('Транспорт' not in names) \
            or ('Мебель' not in names):
            raise ValidationError(
                'Добавьте рубрики недвижимости, транспорта и мебели')


class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=20, label='Искомое слово')
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
                                    label='Рубрика')


class BbCustomForm(forms.Form):
    # Пример поля выбора типа объявления
    KIND_CHOICES = (
        ('b', 'Куплю'),
        ('s', 'Продам'),
        ('c', 'Обменяю'),
    )
    kind = forms.ChoiceField(
        choices=KIND_CHOICES,
        label='Тип объявления'
    )

    # Если вам требуется выбор рубрики из уже существующих
    rubric = forms.ModelChoiceField(
        queryset=Rubric.objects.all(),
        label='Рубрика'
    )

    title = forms.CharField(
        label='Название товара',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Введите название товара'})
    )

    content = forms.CharField(
        label='Описание',
        widget=forms.Textarea(attrs={'placeholder': 'Введите описание товара'})
    )

    price = forms.DecimalField(
        label='Цена',
        max_digits=15,
        decimal_places=2,
        required=False
    )

    # Добавляем капчу
    captcha = CaptchaField(
        label='Введите текст с картинки',
        error_messages={'invalid': 'Неправильный текст'}
    )
