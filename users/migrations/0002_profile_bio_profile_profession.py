# Generated by Django 4.1.7 on 2023-04-16 15:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='profile',
            name='profession',
            field=models.TextField(blank=True,
                                   max_length=100, validators=[django.core.validators.MaxLengthValidator(100)]),
        ),
    ]
