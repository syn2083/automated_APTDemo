from django import forms
from .models import DemoConfig, JIFTemplate
from automated_APTDemo.logging_setup import init_logging

logger = init_logging()


class DemoConfigForm(forms.ModelForm):
    class Meta:
        model = DemoConfig
        fields = ['idc_1_path', 'idc_1_time', 'idc_1_type', 'idc_2_path', 'idc_2_time', 'idc_2_type', 'idc_3_path',
                  'idc_3_time', 'idc_3_type', 'idc_4_path', 'idc_4_time', 'idc_4_type', 'jdf_input_path',
                  'jif_acks_path', 'reprint_path', 'proc_phase_path', 'td_multi_path', 'td_type', 'idc_1_ps', 'idc_2_ps',
                  'idc_3_ps', 'idc_4_ps']


class JIFTemplateForm(forms.ModelForm):
    class Meta:
        model = JIFTemplate
        fields = ['template_name', 'job_type', 'job_number', 'job_class', 'job_name', 'job_prefix', 'account_id',
                  'product_name', 'production_location', 'envelope_id', 'stock_id', 'stock_type', 'user_info_1',
                  'user_info_2', 'user_info_3', 'user_info_4', 'user_info_5', 'contact_email', 'piece_range',
                  'shift_1_operators', 'shift_2_operators', 'shift_3_operators']
