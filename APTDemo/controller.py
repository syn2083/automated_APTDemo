import os
from collections import deque
from . import settings
from automated_APTDemo.logging_setup import init_logging
from .jifgenerator import jif_assembler

"""
This is the Demo Controller Brain.
"""
logger = init_logging()


class DemoController:
    def __init__(self, jdf_folder):
        self.demo_status = 0
        self.icd_1 = []
        self.icd_1_multi = True
        self.icd_2 = []
        self.icd_3 = []
        self.icd_4 = []
        self.td = []
        self.reprint_jobs = {}
        self.completed_jobs = []
        self.data_folder = settings.EXIT_DIR
        self.jif_folder = jdf_folder
        self.first_run = 1

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

    def multi_job(self, jobid=None):
        if not jobid:
            logger.debug('Multi-job processor called with no jobid.')
        if not self.icd_1_multi:
            pass
        if jobid in self.icd_1:
            if self.td:
                logger.debug('Multi-job passing to TD but it is busy.')
                # will try to add, and let next step handle this situation
                self.td.append(jobid)
            else:
                self.td.append(jobid)


    def reprint_request(self, jobid=None):
        pass

    def start_demo(self):
        # clean up any outstanding exit data
        files = os.listdir(self.data_folder)
        logger.debug('Demo Start called, cleaning exit directory.')
        for file in files:
            os.remove(self.data_folder + '/' + file )
        self.first_run = 0
        logger.debug('Setting demo status to 1, starting Demo.')
        self.demo_status = 1
        icd_1 = jif_assembler.JIFBuilder('icd_1', self.jif_folder)
        logger.debug('Creating ICD 1 JIF/Exit Data')
        icd_1.gen_jifs()
        icd_2 = jif_assembler.JIFBuilder('icd_2', self.jif_folder)
        logger.debug('Creating ICD 2 JIF/Exit Data')
        icd_2.gen_jifs()
        icd_3 = jif_assembler.JIFBuilder('icd_3', self.jif_folder)
        logger.debug('Creating ICD 3 JIF/Exit Data')
        icd_3.gen_jifs()
        td = jif_assembler.JIFBuilder('td', self.jif_folder)
        logger.debug('Creating Initial TD JIF/Exit Data')
        td.gen_jifs()
        logger.debug('Demo Initialized.')
        return 'Demo initialization and startup complete.'

    def stop_demo(self):
        logger.debug('Setting demo status to 0, stopping demo.')
        self.demo_status = 0
        self.icd_1 = []
        self.icd_2 = []
        self.icd_3 = []
        self.icd_4 = []
        self.td = []
        # clean up exit data
        files = os.listdir(self.data_folder)
        logger.debug('Cleaning exit directory.')
        for file in files:
            os.remove(self.data_folder + '/' + file)
        logger.debug('Resetting demo state')
        self.first_run = 1
        return 'Demo shut down complete.'


