# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-25 10:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_auto_20161125_1010'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feature',
            options={'verbose_name': 'Тип', 'verbose_name_plural': 'Типи'},
        ),
        migrations.AlterModelOptions(
            name='featuretype',
            options={'verbose_name': 'Типи компонентів', 'verbose_name_plural': 'Типи компоненту'},
        ),
        migrations.AlterField(
            model_name='feature',
            name='feature_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.FeatureType', verbose_name='Довідник типів компонентів'),
        ),
        migrations.AlterField(
            model_name='featuretype',
            name='component_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.ComponentType', verbose_name='Довідник компонентів'),
        ),
    ]