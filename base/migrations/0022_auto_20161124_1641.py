# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-24 14:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_auto_20161122_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='floors',
            field=models.IntegerField(default=1, verbose_name='Кількість поверхів'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='building',
            name='heated_square',
            field=models.IntegerField(default=1, verbose_name='Опалювальна площа'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='building',
            name='heated_volume',
            field=models.IntegerField(default=1, verbose_name="Опалювальний об'єм"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='meterdata',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.datetime_safe.datetime.now, verbose_name='Дата'),
        ),
    ]