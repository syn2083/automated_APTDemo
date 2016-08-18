import logging
from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)

class ProcManager(models.Model):
    id = models.AutoField(primary_key=True)
    jobs_run = models.IntegerField(verbose_name='Total Jobs Processed')
    jobs_last_demo = models.IntegerField(verbose_name='Total Jobs Processed Last Init')
    times_started = models.IntegerField(verbose_name='Demo System Runs')
    last_run_date = models.DateTimeField(default=timezone.now)

    def save_proc_manager(self):
        self.save()
        logger.debug('Process Manager Settings Saved')


class DemoConfig(models.Model):
    id = models.AutoField(primary_key=True)
    idc_1_path = models.CharField(verbose_name='IDC 1 Path', max_length=200)
    idc_1_type = models.CharField(verbose_name='IDC 1 Device Type', max_length=40)
    idc_1_time = models.IntegerField(verbose_name='IDC 1 Scans per hour', max_length=6)
    idc_2_path = models.CharField(verbose_name='IDC 2 Path', max_length=200)
    idc_2_type = models.CharField(verbose_name='IDC 2 Device Type', max_length=40)
    idc_2_time = models.IntegerField(verbose_name='IDC 2 Scans per hour', max_length=6)
    idc_3_path = models.CharField(verbose_name='IDC 3 Path', max_length=200)
    idc_3_type = models.CharField(verbose_name='IDC 3 Device Type', max_length=40)
    idc_3_time = models.IntegerField(verbose_name='IDC 3 Scans per hour', max_length=6)
    idc_4_path = models.CharField(verbose_name='IDC 4 Path', max_length=200)
    idc_4_type = models.CharField(verbose_name='IDC 4 Device Type', max_length=40)
    idc_4_time = models.IntegerField(verbose_name='IDC 4 Scans per hour', max_length=6)
    td_multi_path = models.CharField(verbose_name='TD Input Path', max_length=200)
    td_type = models.CharField(verbose_name='TD Device Type', max_length=40)

    def save_demo(self):
        self.save()
        logger.debug('Demo Settings Saved')


class JIFTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    template_name = models.CharField(max_length=100, default='APTDemo')
    job_prefix = models.CharField(max_length=3)
    account_id = models.CharField(max_length=1000)
    job_name = models.CharField(max_length=1000)
    job_type = models.CharField(max_length=1000)
    job_number = models.CharField(max_length=1000)
    job_class = models.CharField(max_length=1000)
    product_name = models.CharField(max_length=1000)
    production_location = models.CharField(max_length=500)
    envelope_id = models.CharField(max_length=1000)
    stock_id = models.CharField(max_length=1000)
    stock_type = models.CharField(max_length=1000)
    user_info_1 = models.CharField(max_length=1000)
    user_info_2 = models.CharField(max_length=1000)
    user_info_3 = models.CharField(max_length=1000)
    user_info_4 = models.CharField(max_length=1000)
    user_info_5 = models.CharField(max_length=1000)
    contact_email = models.CharField(max_length=1000)
    # Options
    piece_range = models.CharField(max_length=100)
    shift_1_operators = models.CharField(max_length=500)
    shift_2_operators = models.CharField(max_length=500)
    shift_3_operators = models.CharField(max_length=500)
    template_date = models.DateTimeField(default=timezone.now)

    def save_jif(self):
        self.template_date = timezone.now()
        self.save()
        logger.debug('JIF Template Settings Saved')

    def __str__(self):
        return self.template_name
