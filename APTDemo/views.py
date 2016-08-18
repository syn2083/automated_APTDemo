from django.shortcuts import render
from .folder_monitor import folder_monitor_handler as fmh
import threading
import time

threads = []


def worker():
    observer = fmh.Observer()
    observer.schedule(fmh.FolderHandler(), path='C:\APTApplication\Server\Inputs\JIFAcks')
    observer.start()
    print('observer started')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def demo_central(request):
    return render(request, 'APTDemo/demo_central.html', {})
