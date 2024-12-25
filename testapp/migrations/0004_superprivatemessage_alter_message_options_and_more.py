# Generated by Django 5.1.2 on 2024-12-25 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0003_message_privatemessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuperPrivateMessage',
            fields=[
            ],
            options={
                'ordering': ['-published'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('testapp.privatemessage',),
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-published']},
        ),
        migrations.AlterModelOptions(
            name='privatemessage',
            options={'ordering': []},
        ),
    ]
