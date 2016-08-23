import django.http
from automated_APTDemo import logging_setup
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from .controller import DemoController
from .models import DemoConfig, JIFTemplate
from .forms import DemoConfigForm, JIFTemplateForm
from .controller import DemoController
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext

logger = logging_setup.init_logging()
control = DemoController(get_object_or_404(DemoConfig, pk=1).jdf_input_path)


def demo_central(request):
    # demo = get_object_or_404(DemoConfig, pk=1)
    # s = DemoController()
    # s.create_workers(jif_acks_path=demo.jif_acks_path, reprint_path=demo.reprint_path, proc_path=demo.proc_phase_path)
    return render(request, 'APTDemo/demo_central.html', {})


def demo_controls(request):
    if request.method == "GET":
        context = RequestContext(request)
        context_dict = {'demo_status': control.demo_status}
        return render_to_response('APTDemo/demo_controller.html', context_dict, context)
    elif request.method == "POST":
        return render(request, 'APTDemo/demo_controller.html', {'controller': control})


def start_demo(request):
    logger.debug('Start demo request.')
    # reply = control.start_demo()
    reply = 'Started'
    control.demo_status = 1
    return django.http.HttpResponse(reply)


def stop_demo(request):
    logger.debug('Stop demo request.')
    reply = control.stop_demo()
    return django.http.HttpResponse(reply)


def demo_config(request):
    demo = get_object_or_404(DemoConfig, pk=1)
    if request.method == "POST":
        form = DemoConfigForm(request.POST, instance=demo)
        if form.is_valid():
            logger.debug(form.data)
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


@csrf_exempt
def job_accepted(request):
    if request.method == "POST":
        x = request.readlines()
        logger.debug(x[0].decode('utf-8'))
    return render(request, 'APTDemo/job_accepted.html', {})


@csrf_exempt
def reprint_sent(request):
    if request.method == "POST":
        x = request.readlines()
        logger.debug(x[0].decode('utf-8'))
    return render(request, 'APTDemo/reprint_sent.html', {})


@csrf_exempt
def proc_phase(request):
    if request.method == "POST":
        x = request.readlines()
        logger.debug(x[0].decode('utf-8'))
    return render(request, 'APTDemo/proc_phase.html', {})


@csrf_exempt
def job_complete(request):
    if request.method == "POST":
        x = request.readlines()
        logger.debug(x[0].decode('utf-8'))
    return render(request, 'APTDemo/job_complete.html', {})
