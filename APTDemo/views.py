from automated_APTDemo import logging_setup
from django.shortcuts import render, get_object_or_404, redirect
from .controller import DemoController
from .models import DemoConfig, JIFTemplate
from .forms import DemoConfigForm, JIFTemplateForm
from django.http import HttpResponse
from django.template import loader
from django.template import RequestContext
import datetime

logger = logging_setup.init_logging()


def demo_central(request):
    demo = get_object_or_404(DemoConfig, pk=1)
    s = DemoController()
    s.create_workers(jif_acks_path=demo.jif_acks_path, reprint_path=demo.reprint_path, proc_path=demo.proc_phase_path)
    return render(request, 'APTDemo/demo_central.html', {})


def demo_controls(request):
    return render(request, 'APTDemo/demo_controller.html', {})


def demo_config(request):
    demo = get_object_or_404(DemoConfig, pk=1)
    if request.method == "POST":
        form = DemoConfigForm(request.POST, instance=demo)
        if form.is_valid():
            demo = form.save(commit=False)
            demo.save()
    else:
        form = DemoConfigForm(instance=demo)
    return render(request, 'APTDemo/demo_config.html', {'form': form})


def jif_config(request):
    jif = get_object_or_404(JIFTemplate, pk=1)
    if request.method == "POST":
        form = JIFTemplateForm(request.POST, instance=jif)
        if form.is_valid():
            jif = form.save(commit=False)
            jif.save()
    else:
        form = JIFTemplateForm(instance=jif)
    return render(request, 'APTDemo/jif_config.html', {'form': form, 'jif': jif})


def current_times(request):
    context = {'current_time': datetime.datetime.now()}
    template = loader.get_template('APTDemo/home.html')
    data = RequestContext(request, context)
    return HttpResponse(template.render(data))
