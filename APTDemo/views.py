from automated_APTDemo import logging_setup
from django.shortcuts import render

logger = logging_setup.init_logging()


def demo_central(request):
    logger.debug('Testing')
    return render(request, 'APTDemo/demo_central.html', {})
