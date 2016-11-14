# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-14 11:02
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_auto_20161114_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='percentage',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Відсоток від загальної кількості'),
        ),
    ]