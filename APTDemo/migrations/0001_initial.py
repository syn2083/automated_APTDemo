# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-18 15:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DemoConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('idc_1_path', models.CharField(max_length=200, verbose_name='IDC 1 Path')),
                ('idc_1_type', models.CharField(max_length=40, verbose_name='IDC 1 Device Type')),
                ('idc_1_time', models.IntegerField(max_length=6, verbose_name='IDC 1 Scans per hour')),
                ('idc_2_path', models.CharField(max_length=200, verbose_name='IDC 2 Path')),
                ('idc_2_type', models.CharField(max_length=40, verbose_name='IDC 2 Device Type')),
                ('idc_2_time', models.IntegerField(max_length=6, verbose_name='IDC 2 Scans per hour')),
                ('idc_3_path', models.CharField(max_length=200, verbose_name='IDC 3 Path')),
                ('idc_3_type', models.CharField(max_length=40, verbose_name='IDC 3 Device Type')),
                ('idc_3_time', models.IntegerField(max_length=6, verbose_name='IDC 3 Scans per hour')),
                ('idc_4_path', models.CharField(max_length=200, verbose_name='IDC 4 Path')),
                ('idc_4_type', models.CharField(max_length=40, verbose_name='IDC 4 Device Type')),
                ('idc_4_time', models.IntegerField(max_length=6, verbose_name='IDC 4 Scans per hour')),
                ('td_multi_path', models.CharField(max_length=200, verbose_name='TD Input Path')),
                ('td_type', models.CharField(max_length=40, verbose_name='TD Device Type')),
            ],
        ),
        migrations.CreateModel(
            name='JIFTemplate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('template_name', models.CharField(default='APTDemo', max_length=100)),
                ('job_prefix', models.CharField(max_length=3)),
                ('account_id', models.CharField(max_length=1000)),
                ('job_name', models.CharField(max_length=1000)),
                ('job_type', models.CharField(max_length=1000)),
                ('job_number', models.CharField(max_length=1000)),
                ('job_class', models.CharField(max_length=1000)),
                ('product_name', models.CharField(max_length=1000)),
                ('production_location', models.CharField(max_length=500)),
                ('envelope_id', models.CharField(max_length=1000)),
                ('stock_id', models.CharField(max_length=1000)),
                ('stock_type', models.CharField(max_length=1000)),
                ('user_info_1', models.CharField(max_length=1000)),
                ('user_info_2', models.CharField(max_length=1000)),
                ('user_info_3', models.CharField(max_length=1000)),
                ('user_info_4', models.CharField(max_length=1000)),
                ('user_info_5', models.CharField(max_length=1000)),
                ('contact_email', models.CharField(max_length=1000)),
                ('piece_range', models.CharField(max_length=100)),
                ('shift_1_operators', models.CharField(max_length=500)),
                ('shift_2_operators', models.CharField(max_length=500)),
                ('shift_3_operators', models.CharField(max_length=500)),
                ('template_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ProcManager',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('jobs_run', models.IntegerField(verbose_name='Total Jobs Processed')),
                ('jobs_last_demo', models.IntegerField(verbose_name='Total Jobs Processed Last Init')),
                ('times_started', models.IntegerField(verbose_name='Demo System Runs')),
                ('last_run_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
