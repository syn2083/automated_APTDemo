# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-22 20:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APTDemo', '0003_auto_20160818_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='democonfig',
            name='idc_1_multi',
            field=models.IntegerField(default=1, verbose_name='IDC Multi-step'),
        ),
        migrations.AlterField(
            model_name='democonfig',
            name='idc_1_path',
            field=models.CharField(default='C:/APTApplication/IDC/IDC_1', max_length=200, verbose_name='IDC 1 Path'),
        ),
        migrations.AlterField(
            model_name='democonfig',
            name='idc_2_path',
            field=models.CharField(default='C:/APTApplication/IDC/IDC_2', max_length=200, verbose_name='IDC 2 Path'),
        ),
        migrations.AlterField(
            model_name='democonfig',
            name='idc_3_path',
            field=models.CharField(default='C:/APTApplication/IDC/IDC_3', max_length=200, verbose_name='IDC 3 Path'),
        ),
        migrations.AlterField(
            model_name='democonfig',
            name='idc_4_path',
            field=models.CharField(default='C:/APTApplication/IDC/IDC_4', max_length=200, verbose_name='IDC 4 Path'),
        ),
        migrations.AlterField(
            model_name='democonfig',
            name='td_multi_path',
            field=models.CharField(default='C:/APTApplication/IDC/TD', max_length=200, verbose_name='TD Input Path'),
        ),
    ]