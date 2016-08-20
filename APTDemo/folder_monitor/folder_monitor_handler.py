import time
import sys
import os
import shutil
from automated_APTDemo import logging_setup
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from django.shortcuts import get_object_or_404
from APTDemo.models import DemoConfig

logger = logging_setup.init_logging()


class FolderHandler(PatternMatchingEventHandler):
    jif_proc_pattern = ['*.accepted']
    reprint_pattern = ['*.txt']
    proc_xml_pattern = ['*.xml']

    def __init__(self, controller):
        super().__init__()
        self.master = controller

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        logger.debug('{}{}'.format(event.src_path, event.event_type))
        filename = str(event.src_path).split('\\')[-1]
        if 'accepted' in filename.split('.'):
            print('JIF {} accepted, proceeding...'.format(filename.split('.')[0]))
            exit_name = 'exit_{}.txt'.format(filename.split('.')[0])
            if os.path.exists(os.path.join(self.master.datafolder, exit_name)):
                print('Exit data exists, copying!')
                shutil.copy(os.path.join(self.master.datafolder, exit_name),
                            os.path.join('C:\\APTApplication\\ICD\\TDInput', exit_name))
                print('Trackdevice should be running now!')
        if 'txt' in filename.split('.'):
            pass
        if 'xml' in filename.split('.'):
            pass

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

