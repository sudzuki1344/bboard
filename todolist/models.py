from django.db import models
from django.core import  validators
from django.core.exceptions import ValidationError
from django.db import models

class Todo(models.Model):

    title = models.CharField(
        max_length=50,
        verbose_name='Задача'
    )

    content = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
    )

    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Опубликовано',
    )