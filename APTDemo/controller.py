import logging
import threading
import time
from .folder_monitor import folder_monitor_handler as fmh

"""
This is the Demo Controller Brain.
"""
logger = logging.getLogger(__name__)


class DemoController():
    def __init__(self):
        self.demo_status = 0
        self.currently_running = {}
        self.reprint_jobs = {}
        self.completed_jobs = []
        self.data_folder = ''
        self.idc_folders = {}
        self.jdf_folder = ''
        self.jif_ack_folder = ''
        self.reprint_folder = ''
        self.monitor_threads = {'Folder': None}

    def __repr__(self):
        if self.demo_status == 0:
            return 'Not Running'
        if self.demo_status == 1:
            return 'Running'
        if self.demo_status == 2:
            return 'Paused'

    def worker(self):
        observer = fmh.Observer()
        observer.schedule(fmh.FolderHandler(), path='C:\APTApplication\Server\Inputs\JIFAcks')
        observer.start()
        print('observer started')
        try:
            while True:
                time.sleep(1)
        except SystemExit:
            observer.stop()

        observer.join()
