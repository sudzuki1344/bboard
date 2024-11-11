from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models

from bboard.models import validation_even

class Rubric(models.Model):
    name = models.CharField(
        unique=True,
        max_length=20,
        db_index=True,
        verbose_name='Название',
    )

    def __str__(self):
        return f'{self.name}'

    # def get_absolut_url(self):
    #     return f"{self.pk}/"

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    # def delete(self, *args, **kwargs):
    #     super().delete(self, *args, **kwargs)



    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'

class Aa(models.Model):
    # KINDS = (
    #     ('b', 'Куплю'),
    #     ('s', 'Продам'),
    #     ('c', 'Обменяю'),
    # )

    KINDS = (
        (None, 'Выберите тип публикуемого объявления'),
        ('b', 'Куплю'),
        ('s', 'Продам'),
        ('c', 'Обменяю'),
        ('a', 'Отдам')
    )

    # KINDS = (
    #     ('Купля-продажа', (
    #         ('b', 'Куплю'),
    #         ('s', 'Продам'),
    #     )),
    #     ('Обмен', (
    #         ('c', 'Обменяю'),
    #     ))
    # )

    kind = models.CharField(
        max_length=1,
        choices=KINDS,
        default='b',
    )

    # rubric = models.ForeignKey(
    #     'Rubric',
    #     null=True,
    #     on_delete=models.PROTECT,
    #     verbose_name='Рубрика',
    # )

    title = models.CharField(
        max_length=50,
        verbose_name='Товар',
        validators=[validators.RegexValidator(regex='^.{4,}$')],
        error_messages={'invalid': 'Введите 4 и более символа'},
    )

    content = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
        validators=[validators.RegexValidator(regex='^.{5,}$')],
        error_messages={'invalid': 'Введите 5 и более символа'}
    )

    # price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        default=0,
        verbose_name='Цена',
        validators=[validation_even]
    )

    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Опубликовано',
    )

    # is_active = models.BooleanField()
    # email = models.EmailField()
    # url = models.URLField()
    # slug = models.SlugField()

    def title_and_price(self):
        if self.price:
            return f"{self.title} ({self.price:.2f} тг.)"
        return self.title

    title_and_price.short_description = 'Название и цена'

    def clean(self):
        errors = {}
        if not self.content:
            errors['content'] = ValidationError('Укажите описание товара')
        if self.price and self.price < 0:
            errors['price'] = ValidationError('Укажите неотрицательное значение цены')
        if not self.title:
            errors['title'] = ValidationError('Напишите название товара')
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f'{self.title} ({self.price} тг.)'

    class Meta:
        ordering = ['-published', 'title']
        unique_together = ('title', 'published')
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

