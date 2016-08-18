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

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed here
        exit_folder = "C:\\Users\\trogers\\PycharmProjects\\StandaloneJIF\\output\\Testing_8_17\\exit_data"
        print(event.src_path, event.event_type)
        filename = str(event.src_path).split('\\')[-1]
        if 'accepted' in filename.split('.'):
            print('JIF {} accepted, proceeding...'.format(filename.split('.')[0]))
            exit_name = 'exit_{}.txt'.format(filename.split('.')[0])
            if os.path.exists(os.path.join(exit_folder, exit_name)):
                print('Exit data exists, copying!')
                shutil.copy(os.path.join(exit_folder, exit_name),
                            os.path.join('C:\\APTApplication\\ICD\\TDInput', exit_name))
                print('Trackdevice should be running now!')

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

