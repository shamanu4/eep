# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-24 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_auto_20161124_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='floor_height',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=3, verbose_name='Висота поверху'),
            preserve_default=False,
        ),
    ]