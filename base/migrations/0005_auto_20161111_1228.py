# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-11 10:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20161111_1157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Iдентифікатор лічильника')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
            ],
            options={
                'verbose_name': 'Лічильник',
                'verbose_name_plural': 'Лічильники',
            },
        ),
        migrations.CreateModel(
            name='MeterData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prev_data', models.DecimalField(decimal_places=3, max_digits=9, verbose_name='Попередні дані')),
                ('cur_data', models.DecimalField(decimal_places=3, max_digits=9, verbose_name='Поточні дані')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Відповідальна особа')),
                ('meter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Meter', verbose_name='Лічильник')),
            ],
            options={
                'verbose_name': 'Показник лічильника',
                'verbose_name_plural': 'Показники лічильників',
            },
        ),
        migrations.CreateModel(
            name='MeterType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Тип лічильника')),
                ('unit', models.CharField(max_length=50, verbose_name='Одиниця виміру')),
            ],
            options={
                'verbose_name': 'Тип лічильника',
                'verbose_name_plural': 'Типи лічильників',
            },
        ),
        migrations.AlterField(
            model_name='building',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Institution', verbose_name='Заклад'),
        ),
        migrations.AlterField(
            model_name='building',
            name='name',
            field=models.CharField(max_length=500, verbose_name='Будівля'),
        ),
        migrations.AddField(
            model_name='meter',
            name='building',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Building', verbose_name='Будівля'),
        ),
        migrations.AddField(
            model_name='meter',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Institution', verbose_name='Заклад'),
        ),
        migrations.AddField(
            model_name='meter',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='base.Meter', verbose_name='Орендодавець'),
        ),
    ]