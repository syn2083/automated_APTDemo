from os import path
import datetime
from django.shortcuts import get_object_or_404

__author__ = 'venom'


class Template(object):
    def __init__(self, **kwargs):
        self.initial_seed = '0000001'
        self.site_prefix = kwargs['site_prefix']
        self.template_name = kwargs['name']
        self.piece_level = kwargs['piece_level']
        self.var_pieces = kwargs['var_pieces']
        self.piece_range = kwargs['piece_range']
        self.var_sheets = kwargs['var_sheets']
        self.sheet_range = kwargs['sheet_range']
        self.num_jifs = kwargs['num_jifs']
        self.job_id = kwargs['job_id']
        self.account = kwargs['account']
        self.job_name = kwargs['job_name']
        self.job_type = kwargs['job_type']
        self.num_pieces = kwargs['num_pieces']
        self.num_sheets = kwargs['num_sheets']
        self.creation = kwargs['creation']
        self.deadline = kwargs['deadline']
        self.proc_phase = kwargs['proc_phase']
        self.end_phase = kwargs['end_phase']
        self.prod_loc = kwargs['prod_loc']
        self.feed_data = kwargs['feed_data']
        self.exit_data = kwargs['exit_data']
        self.damages = kwargs['damages']
        self.userinfo1 = kwargs['userinfo1']
        self.userinfo2 = kwargs['userinfo2']
        self.userinfo3 = kwargs['userinfo3']
        self.userinfo4 = kwargs['userinfo4']
        self.userinfo5 = kwargs['userinfo5']
        self.jobclass = kwargs['class']
        self.imp_mult = kwargs['imp_mult']
        self.icd_mode = kwargs['icd_mode']
        self.feed_operators = kwargs['feed_ops']
        self.exit_operators = kwargs['exit_ops']
        self.replacements = kwargs['replacements']
        self.current_jobid = None
        self.current_piececount = None
        self.generated_jobs = None
        self.curr_feed_time = None
        self.curr_exit_time = None
        self.damage_count = 0
        self.current_bad = 0

    def id_to_int(self):
        try:
            return int(self.job_id)
        except ValueError:
            return None

    def id_to_str(self, input_id):
        try:
            return str(input_id).zfill(7)
        except:
            return None

    def jobid_loader(self):
        local_path = path.dirname(path.abspath(__file__))
        seeder = path.join(local_path, "job_seed.txt")
        if not path.isfile('job_seed.txt'):
            with open(seeder, 'w') as fp:
                fp.write('0000001')
            fp.close()
            self.current_jobid = 1
        else:
            with open(seeder, 'r') as fp:
                self.current_jobid = int(fp.read())
            fp.close()

    def jobid_saver(self):
        local_path = path.dirname(path.abspath(__file__))
        seeder = path.join(local_path, "job_seed.txt")
        if not path.isfile('job_seed.txt'):
            with open(seeder, 'w') as fp:
                fp.write('0000001')
            fp.close()
        else:
            with open(seeder, 'w') as fp:
                fp.write(str(self.current_jobid))
            fp.close()

    def add_seconds(self, in_time, secs):
        fulldate = in_time
        newtime = fulldate + datetime.timedelta(seconds=secs)
        return newtime
