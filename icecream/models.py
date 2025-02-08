from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class IceCreamStand(models.Model):
    """Модель киоска с мороженым"""
    name = models.CharField(max_length=100, verbose_name='Название киоска')
    location = models.CharField(max_length=200, verbose_name='Адрес')
    working_hours = models.CharField(max_length=100, verbose_name='Часы работы')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self):
        return f"{self.name} ({self.location})"

    class Meta:
        verbose_name = 'Киоск с мороженым'
        verbose_name_plural = 'Киоски с мороженым'
        ordering = ['name']


class IceCream(models.Model):
    """Модель мороженого"""
    TYPES = [
        ('cone', 'Рожок'),
        ('cup', 'Стаканчик'),
        ('stick', 'На палочке'),
        ('bulk', 'Весовое'),
    ]

    name = models.CharField(max_length=100, verbose_name='Название')
    type = models.CharField(max_length=10, choices=TYPES, verbose_name='Тип')
    flavor = models.CharField(max_length=50, verbose_name='Вкус')
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Цена'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    is_available = models.BooleanField(default=True, verbose_name='В наличии')
    
    # Связь с киоском (многие к одному)
    stand = models.ForeignKey(
        IceCreamStand,
        on_delete=models.CASCADE,
        related_name='ice_creams',
        verbose_name='Киоск'
    )

    def __str__(self):
        return f"{self.name} ({self.get_type_display()}) - {self.flavor}"

    class Meta:
        verbose_name = 'Мороженое'
        verbose_name_plural = 'Мороженое'
        ordering = ['name', 'type']


class Parent(models.Model):
    """Модель родителя"""
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.CharField(max_length=200, verbose_name='Адрес')

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = 'Родитель'
        verbose_name_plural = 'Родители'
        ordering = ['last_name', 'first_name']


class Child(models.Model):
    """Модель ребёнка"""
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    birth_date = models.DateField(verbose_name='Дата рождения')
    
    # Связь с родителем (многие к одному)
    parent = models.ForeignKey(
        Parent,
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name='Родитель'
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = 'Ребёнок'
        verbose_name_plural = 'Дети'
        ordering = ['last_name', 'first_name']
