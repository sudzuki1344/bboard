# Generated by Django 5.1.2 on 2024-11-11 11:51

import bboard.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0004_alter_bb_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bb',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True, validators=[bboard.models.validation_even], verbose_name='Цена'),
        ),
    ]
