# Generated by Django 3.2 on 2024-09-08 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20240907_2102'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('username', 'role'), 'verbose_name': 'пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
