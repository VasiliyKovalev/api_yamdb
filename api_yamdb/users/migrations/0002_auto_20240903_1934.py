# Generated by Django 3.2 on 2024-09-03 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=254, unique=True, verbose_name='Электронная почта'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(username='me'), name='username_not_me'),
        ),
    ]
