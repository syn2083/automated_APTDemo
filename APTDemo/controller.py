import threading
import time
from .folder_monitor import folder_monitor_handler as fmh
from automated_APTDemo.logging_setup import init_logging

"""
This is the Demo Controller Brain.
"""
logger = init_logging()


class DemoController:
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
        self.monitor_threads = {'jif_observer': None, 'reprint_observer': None, 'proc_observer': None, 'holder': None}

    def __repr__(self):
        if self.demo_status == 0:
            return 'Not Running'
        if self.demo_status == 1:
            return 'Running'
        if self.demo_status == 2:
            return 'Paused'

    def remove_job(self, idc=None, jobid=None):
        pass

    def add_job(self, jobid=None):
        pass

    def observer_thread(self):
        try:
            time.sleep(1)
        except SystemExit:
            self.monitor_threads['jif_observer'].stop()
            self.monitor_threads['reprint_observer'].stop()
            self.monitor_threads['proc_observer'].stop()
        self.monitor_threads['jif_observer'].join()
        self.monitor_threads['reprint_observer'].join()
        self.monitor_threads['proc_observer'].join()

    def create_workers(self, jif_acks_path=None, reprint_path=None, proc_path=None,):
        logger.debug('Setting up monitor workers')
        jif_observer = fmh.Observer()
        self.monitor_threads['jif_observer'] = jif_observer
        jif_observer.schedule(fmh.FolderHandler(), path='{}'.format(jif_acks_path))
        jif_observer.start()
        reprint_observer = fmh.Observer()
        self.monitor_threads['reprint_observer'] = reprint_observer
        reprint_observer.schedule(fmh.FolderHandler(), path='{}'.format(reprint_path))
        reprint_observer.start()
        proc_observer = fmh.Observer()
        self.monitor_threads['proc_observer'] = proc_observer
        proc_observer.schedule(fmh.FolderHandler(), path='{}'.format(proc_path))
        proc_observer.start()
        t = threading.Thread(target=self.observer_thread)
        self.monitor_threads['holder'] = t
        t.start()

