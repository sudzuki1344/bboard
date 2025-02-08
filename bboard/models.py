from datetime import datetime
from os.path import splitext

from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from .validators import validate_non_negative


# from precise_bbcode.fields import BBCodeTextField


def get_timestamp_path(instance, filename):
    # return '%s%s' % (datetime.now().timestamp(),
    #                  splitext(filename)[1])
    return f'{datetime.now().timestamp()}{splitext(filename)[1]}'

def validate_even(val):
    if val % 2 != 0:
        raise ValidationError('Число %(value)s нечётное', code='odd',
                              params={'value': val})


class MinMaxValueValidator:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, val):
        if val < self.min_value or val > self.max_value:
            raise ValidationError('Введённое число должно'
                  'находиться в диапазоне от %(min)s до %(max)s',
                  code='out_of_range',
                  params={'min': self.min_value, 'max': self.max_value})


class Img(models.Model):
    img = models.ImageField(verbose_name='Изображение',
                            upload_to=get_timestamp_path)
    desc = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class RubricQuerySet(models.QuerySet):
    def order_by_bb_count(self):
        return self.annotate(
            cnt=models.Count('bb')).order_by('-cnt')


class RubricManager(models.Manager):
    # def get_queryset(self):
    #     return super().get_queryset().order_by('order', 'name')

    # def order_by_bb_count(self):
    #     return super().get_queryset().annotate(
    #         cnt=models.Count('bb')).order_by('-cnt')

    def get_queryset(self):
        return RubricQuerySet(self.model, using=self._db)

    def order_by_bb_count(self):
        return self.get_queryset().order_by_bb_count()


class Rubric(models.Model):
    name = models.CharField(
        unique=True,
        max_length=20,
        db_index=True,
        verbose_name='Название',
    )

    order = models.SmallIntegerField(default=0, db_index=True)

    # objects = models.Manager()
    # bbs = RubricManager()

    # objects = RubricManager()

    # objects = RubricQuerySet.as_manager()
    objects = models.Manager.from_queryset(RubricQuerySet)()

    def get_info(self):
        """Возвращает id и название рубрики"""
        return f'#{self.id}: {self.name}'

    def get_total_price(self):
        """Возвращает сумму цен всех объявлений в рубрике"""
        return sum(bb.price or 0 for bb in self.bb_set.all())

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ['order', 'name']


# 3. Прокси-модели
class RevRubric(Rubric):
    class Meta:
        proxy = True
        ordering = ['-name']


class BbManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('price')


class Bb(models.Model):
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
        default='s',
    )

    rubric = models.ForeignKey(
        'Rubric',
        null=True,
        on_delete=models.PROTECT,
        verbose_name='Рубрика',
        # related_name='entries',  # вместо bb_set
    )

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
    )

    # content = BBCodeTextField(
    #     null=True,
    #     blank=True,
    #     verbose_name='Описание',
    # )

    # price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        default=0,
        verbose_name='Цена',
        validators=[validate_non_negative]
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

    # archive = models.FileField(upload_to='archives/')
    # archive = models.FileField(upload_to='archives/%Y/%m/%d/')
    # file = models.FileField(upload_to=get_timestamp_path)

    img = models.ImageField(blank=True,
                            upload_to=get_timestamp_path,
                            verbose_name='Изображение')

    # thumb = ThumbnailerImageField(
    #     resize_source={'size': (400, 300), 'crop': 'scale'},
    # )

    objects = models.Manager()
    by_price = BbManager()

    def title_and_price(self):
        if self.price:
            return f'{self.title} ({self.price:.2f} тг.)'
        return self.title

    title_and_price.short_description = 'Название и цена'

    def get_full_info(self):
        """Возвращает id и полную информацию об объявлении"""
        return f'#{self.id}: {self.title} ({self.get_kind_display()})'

    def get_total_with_tax(self, tax_rate=0.2):
        """Возвращает цену с учетом налога"""
        if self.price:
            return float(self.price) * (1 + tax_rate)
        return 0

    def clean(self):
        errors = {}
        if not self.content:
            errors['content'] = ValidationError('Укажите описание товара')

        if self.price and self.price < 0:
            errors['price'] = ValidationError('Укажите неотрицательное значение цены')
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f'{self.title} ({self.price} тг.)'

    class Meta:
        ordering = ['-published', 'title']
        # order_with_respect_to = 'rubric'

        unique_together = ('title', 'published')
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
