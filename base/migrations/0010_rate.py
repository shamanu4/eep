# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-14 10:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_building_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Тариф')),
                ('date_from', models.DateField(verbose_name='Тариф дійсний з')),
                ('date_until', models.DateField(blank=True, null=True, verbose_name='Тариф дійсний до')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Category', verbose_name='Категорія')),
                ('meter_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.MeterType', verbose_name='Тип лічильника')),
            ],
            options={
                'verbose_name_plural': 'Тарифи',
                'verbose_name': 'Тариф',
            },
        ),
    ]
