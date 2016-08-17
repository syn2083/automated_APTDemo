from django.shortcuts import render


def demo_central(request):
    return render(request, 'APTDemo/demo_central.html', {})
