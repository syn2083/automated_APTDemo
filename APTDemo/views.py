from automated_APTDemo import logging_setup
from django.shortcuts import render, get_object_or_404, redirect
from .controller import DemoController
from .models import DemoConfig
from .forms import DemoConfigForm, JIFTemplateForm

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
            return redirect('demo_config', pk=demo.pk)
    else:
        form = DemoConfigForm(instance=demo)
    return render(request, 'APTDemo/demo_config.html', {'form': form})
