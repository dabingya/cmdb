# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-12 10:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0013_auto_20180411_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='kernel_version',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='内核版本'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='mem',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='内存'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='release',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='系统版本'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='swap',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='swap'),
        ),
        migrations.AlterField(
            model_name='disk_info',
            name='size',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='磁盘大小'),
        ),
        migrations.AlterField(
            model_name='domain',
            name='datetime',
            field=models.DateField(default='2018-04-12', verbose_name='到期时间'),
        ),
        migrations.AlterField(
            model_name='idc',
            name='create_at',
            field=models.DateField(default='2018-04-12', verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='team',
            name='create_at',
            field=models.DateField(default='2018-04-12', verbose_name='创建时间'),
        ),
    ]
