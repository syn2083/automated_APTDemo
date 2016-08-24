import os
import shutil
from collections import deque
from . import settings
from automated_APTDemo.logging_setup import init_logging
from .jifgenerator import jif_assembler

"""
This is the Demo Controller Brain.
"""
logger = init_logging()


class DemoController:
    def __init__(self, jdf_folder, icd_folders):
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
        self.target_dirs = {'icd_1': icd_folders[0], 'icd_2': icd_folders[1], 'icd_3': icd_folders[2],
                            'icd_4': icd_folders[3], 'td': icd_folders[4]}

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
        icd_1 = jif_assembler.JIFBuilder('icd_1', self.jif_folder, 1)
        logger.debug('Creating ICD 1 JIF/Exit Data')
        self.icd_1.append(icd_1.gen_jifs())
        icd_2 = jif_assembler.JIFBuilder('icd_2', self.jif_folder, None)
        logger.debug('Creating ICD 2 JIF/Exit Data')
        self.icd_2.append(icd_2.gen_jifs())
        icd_3 = jif_assembler.JIFBuilder('icd_3', self.jif_folder, None)
        logger.debug('Creating ICD 3 JIF/Exit Data')
        self.icd_3.append(icd_3.gen_jifs())
        td = jif_assembler.JIFBuilder('td', self.jif_folder, None)
        logger.debug('Creating Initial TD JIF/Exit Data')
        self.td.append(td.gen_jifs())
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

    def new_job(self, data):
        jobid = None
        for item in data.split('&'):
            if 'jobid' in item:
                jobid = item.split('=')[1]

        if jobid in self.icd_1:
            logger.debug('Copying {} to target directory')
            exit_dir = self.data_folder
            data_file = os.path.join(exit_dir, 'sheet_{}.txt'.format(jobid))
            logger.debug('Copying {} to target directory'.format(jobid))
            target = os.path.join(self.target_dirs['icd_1'], 'sheet_{}.txt'.format(jobid))
            shutil.copyfile(data_file, target)
        if jobid in self.icd_2:
            exit_dir = self.data_folder
            data_file = os.path.join(exit_dir, 'piece_{}.txt'.format(jobid))
            logger.debug('Copying {} to target directory'.format(jobid))
            target = os.path.join(self.target_dirs['icd_2'], 'piece_{}.txt'.format(jobid))
            shutil.copyfile(data_file, target)
        if jobid in self.icd_3:
            exit_dir = self.data_folder
            data_file = os.path.join(exit_dir, 'piece_{}.txt'.format(jobid))
            logger.debug('Copying {} to target directory'.format(jobid))
            target = os.path.join(self.target_dirs['icd_3'], 'piece_{}.txt'.format(jobid))
            shutil.copyfile(data_file, target)
        if jobid in self.icd_4:
            pass
        if jobid in self.td:
            exit_dir = self.data_folder
            data_file = os.path.join(exit_dir, 'piece_{}.txt'.format(jobid))
            logger.debug('Copying {} to target directory'.format(jobid))
            target = os.path.join(self.target_dirs['td'], 'piece_{}.txt'.format(jobid))
            shutil.copyfile(data_file, target)

    def proc_phase(self, data):
        jobid = None
        phase = None
        for item in data.split('&'):
            if 'jobid' in item:
                jobid = item.split('=')[1]
            if 'status' in item:
                phase = item.split('=')[1]

        if '1026' in phase or '1030' in phase:
            if jobid in self.icd_1:
                logger.debug('Multi process change from print to insert - removing {}'.format(jobid))
                if self.td:
                    logger.debug('Multi process collision detected in TD.')
                self.td = self.icd_1.pop()
                exit_dir = self.data_folder
                data_file = os.path.join(exit_dir, 'piece_{}.txt'.format(jobid))
                target = os.path.join(self.target_dirs['td'], 'piece_{}.txt'.format(jobid))
                shutil.copyfile(data_file, target)
                logger.debug('Cleaning print data.')
                os.remove(os.path.join(exit_dir, 'sheet_{}.txt'.format(jobid)))
        else:
            pass

    def reprint_job(self, data):
        jobid = None
        for item in data.split('&'):
            if 'jobid' in item:
                jobid = item.split('=')[1]

        if jobid in self.icd_1:
            logger.debug('ICD1 transition not complete - reprint call {}'.format(jobid))

        else:
            if jobid in self.icd_2:
                logger.debug('Transferring ICD2 reprint {}'.format(jobid))
                self.icd_4.append(self.icd_2.pop())
            if jobid in self.icd_3:
                logger.debug('Transferring ICD3 reprint {}'.format(jobid))
                self.icd_4.append(self.icd_3.pop())
            if jobid in self.td:
                logger.debug('Transferring TD reprint {}'.format(jobid))
                self.icd_4.append(self.td.pop())
            exit_dir = self.data_folder
            data_file = os.path.join(exit_dir, 'reprint_{}.txt'.format(jobid))
            logger.debug('Copying {} to reprint directory'.format(jobid))
            target = os.path.join(self.target_dirs['icd_4'], 'reprint_{}.txt'.format(jobid))
            shutil.copyfile(data_file, target)

    def complete_job(self, data):
        jobid = None
        for item in data.split('&'):
            if 'jobid' in item:
                jobid = item.split('=')[1]

        exit_dir = self.data_folder
        files = [os.path.join(exit_dir, 'piece_{}.txt'.format(jobid)),
                 os.path.join(exit_dir, 'sheet_{}.txt'.format(jobid)),
                 os.path.join(exit_dir, 'reprint_{}.txt'.format(jobid))]

        logger.debug('Cleaning old job data.')

        self.completed_jobs.append(jobid)

        for file in files:
            if os.path.exists(file):
                os.remove(file)

        if 'A4' in jobid:
            if jobid in self.td:
                logger.debug('Initial TD job completed: {}'.format(self.td.pop()))
            if jobid in self.icd_4:
                self.icd_4.remove(jobid)

        if 'A1' in jobid:
            self.icd_1.remove(jobid)
            icd_1 = jif_assembler.JIFBuilder('icd_1', self.jif_folder, 1)
            logger.debug('Creating ICD 1 JIF/Exit Data')
            self.icd_1.append(icd_1.gen_jifs())
        if 'A2' in jobid:
            icd_2 = jif_assembler.JIFBuilder('icd_2', self.jif_folder, None)
            logger.debug('Creating ICD 2 JIF/Exit Data')
            self.icd_2.append(icd_2.gen_jifs())
        if 'A3' in jobid:
            icd_3 = jif_assembler.JIFBuilder('icd_3', self.jif_folder, None)
            logger.debug('Creating ICD 3 JIF/Exit Data')
            self.icd_3.append(icd_3.gen_jifs())
