# Generated by Django 5.1.2 on 2025-01-08 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0005_alter_rubric_options_rubric_order_alter_bb_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='RevRubric',
            fields=[
            ],
            options={
                'ordering': ['-name'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('bboard.rubric',),
        ),
    ]
