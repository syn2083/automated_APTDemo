from random import choice, randint
from os import path
from .jif_templater import Template
from .prog_utilities import folder_construct, str_to_list, find_shift
from .. import settings

__author__ = 'venom'

"""This module handles utilizing a JIF Template to produce output. It has builtin assemblers for the
job ticket and piece manifesting, feed scan data, and exit scan data where appropriate. The output data will be placed
in a local directory in the following format:
Output
-TemplateName
--feed_data
--exit_data
--jif_output"""


class JIFBuilder(Template):
    def __init__(self, icd_target, jdf_folder, **kwargs):
        super().__init__(**kwargs)
        self.out = jdf_folder
        if icd_target == 'icd_1':
            self.site_prefix = 'A10'
        if icd_target == 'icd_2':
            self.site_prefix = 'A20'
        if icd_target == 'icd_3':
            self.site_prefix = 'A30'
        if icd_target == 'icd_4':
            self.site_prefix = 'A40'
        if icd_target == 'td':
            self.site_prefix = 'A50'

    def piece_builder(self, piece_id):
        plist = []
        bstr = "\n"

        plist.append("   <Piece>")
        plist.append("    <ID>{pieceid}</ID>".format(pieceid=str(piece_id).zfill(6)))

        if not int(self.var_sheets):
            sheet_count = self.num_sheets
            plist.append("    <TotalSheets>2</TotalSheets>")
        else:
            rlist = [i.strip() for i in self.sheet_range.split(',')]
            sheet_count = randint(int(rlist[0]), int(rlist[1]))
            plist.append("    <TotalSheets>{totals}</TotalSheets>".format(totals=str(sheet_count)))
        plist.append("   </Piece>")
        return [bstr.join(plist), sheet_count]

    def gen_jifs(self):
        bstr = "\n"
        make_damages = 0

        if not self.current_jobid:
            self.jobid_loader()
        conv_dict = {'job_type': [self.job_type, None],
                     'job_name': [self.job_name, None],
                     'account': [self.account, None],
                     'jobclass': [self.jobclass, None],
                     'imp_mult': [self.imp_mult, None],
                     'userinfo1': [self.userinfo1, None],
                     'userinfo2': [self.userinfo2, None],
                     'userinfo3': [self.userinfo3, None],
                     'userinfo4': [self.userinfo4, None],
                     'userinfo5': [self.userinfo5, None],
                     'shift_1_ops': [self.shift_1_operators, None],
                     'shift_2_ops': [self.shift_2_operators, None],
                     'shift_3_ops': [self.shift_3_operators, None]}

        for k,v in conv_dict.items():
            v[1] = str_to_list(v[0])

        if self.damages:
            dc = randint(1, 10)
            self.damage_count = (self.num_jifs * (dc / 100))
            if self.damage_count < 1:
                self.damage_count = 1

        for i in range(0, self.num_jifs):
            if not self.generated_jobs:
                self.generated_jobs = 0
            if self.damages:
                if self.current_bad <= self.damage_count:
                    make_damages = 1
                    self.current_bad += 1
                else:
                    make_damages = 0
            jif_strings = []
            sheet_list = []
            jif_strings.append("""<?xml version="1.0" encoding="UTF-8"?>\n <JobTicket>\n <Version>2.2</Version>""")
            jif_strings.append(" <JobID>{pref}{jobid}</JobID>".format(pref=self.site_prefix,
                                                                      jobid=self.id_to_str(self.current_jobid)))
            jif_strings.append(" <JobType>{jobtype}</JobType>".format(jobtype=choice(conv_dict['job_type'][1])))
            jif_strings.append(" <JobName>{jobname}</JobName>".format(jobname=choice(conv_dict['job_name'][1])))
            jif_strings.append(" <AccountID>{accountid}</AccountID>".format(accountid=choice(conv_dict['account'][1])))
            jif_strings.append(" <StartSequence>000001</StartSequence>")
            count = [i.strip() for i in self.piece_range.split(',')]
            self.current_piececount = randint(int(count[0]), int(count[1]))
            jif_strings.append(" <EndSequence>{lastnumber}</EndSequence>".format(lastnumber=
                                                                                 str(self.current_piececount)
                                                                                 .zfill(6)))
            jif_strings.append(" <PieceCount>{piececount}</PieceCount>".format(piececount=
                                                                               str(self.current_piececount)))
            jif_strings.append(" <CreationDate>{creation}</CreationDate>".format(creation=self.creation[0]))
            jif_strings.append(" <JobDeadLine>{deadline}</JobDeadLine>".format(deadline=self.deadline))
            jif_strings.append(" <PrintMode>1</PrintMode>\n <PageComposition>2</PageComposition>")
            jif_strings.append(" <ProcessingPhases>{pphase}</ProcessingPhases>".format(pphase=self.proc_phase))
            jif_strings.append(" <EndProcess>{endproc}</EndProcess>".format(endproc=self.end_phase))
            jif_strings.append(" <ProductionLocation>{prodloc}</ProductionLocation>".format(prodloc=self.prod_loc))
            jif_strings.append(" <Class>{job_class}</Class>".format(job_class=choice(conv_dict['jobclass'][1])))
            jif_strings.append(" <UserInfo1>{u1}</UserInfo1>".format(u1=choice(conv_dict['userinfo1'][1])))
            jif_strings.append(" <UserInfo2>{u2}</UserInfo2>".format(u2=choice(conv_dict['userinfo2'][1])))
            jif_strings.append(" <UserInfo3>{u3}</UserInfo3>".format(u3=choice(conv_dict['userinfo3'][1])))
            jif_strings.append(" <UserInfo4>{u4}</UserInfo4>".format(u4=choice(conv_dict['userinfo4'][1])))
            jif_strings.append(" <UserInfo5>{u5}</UserInfo5>".format(u5=choice(conv_dict['userinfo5'][1])))
            jif_strings.append("  <JobManifest>")
            for t in range(1, self.current_piececount + 1):
                result = self.piece_builder(t)
                jif_strings.append(result[0])
                sheet_list.append(result[1])
            jif_strings.append("  </JobManifest>")
            multi = int(choice(conv_dict['imp_mult'][1]))
            sheets = 0
            for x in sheet_list:
                sheets += x
            scount = sheets
            jif_strings.append(" <SheetCount>{sheet_count}</SheetCount>".format(sheet_count=scount))
            jif_strings.append(" <PageCount>{page_count}</PageCount>".format(page_count=(multi * scount)))
            jif_strings.append(" </JobTicket>\n")
            jstr = bstr.join(jif_strings)
            filename = path.join(out_jif, self.site_prefix + self.id_to_str(self.current_jobid) + ".jif")
            with open(filename, 'w') as fp:
                fp.write(jstr)
            fp.close()
            if self.exit_data == 1:
                if make_damages:
                    if find_shift() == 1:
                        self.gen_exit_data(create_damages=1, ops=choice(conv_dict['shift_1_ops'][1]))
                    if find_shift() == 2:
                        self.gen_exit_data(create_damages=1, ops=choice(conv_dict['shift_2_ops'][1]))
                    if find_shift() == 3:
                        self.gen_exit_data(create_damages=1, ops=choice(conv_dict['shift_3_ops'][1]))
                else:
                    if find_shift() == 1:
                        self.gen_exit_data(ops=choice(conv_dict['shift_1_ops'][1]))
                    if find_shift() == 2:
                        self.gen_exit_data(ops=choice(conv_dict['shift_2_ops'][1]))
                    if find_shift() == 3:
                        self.gen_exit_data(ops=choice(conv_dict['shift_3_ops'][1]))
            self.current_jobid += 1
            self.generated_jobs += 1
            if self.generated_jobs == self.num_jifs:
                self.jobid_saver()

    def gen_feed_data(self, num_sheets=None, ops=None):
        out_str = "\n"
        out_path = folder_construct(self.template_name)[1]
        sheet_strings = []
        job_string = self.site_prefix + str(self.current_jobid).zfill(7)
        self.curr_feed_time = self.creation[1]

        for i in range(1, self.current_piececount + 1):
            for t in range(1, num_sheets[i - 1] + 1):
                if self.icd_mode:
                    sheet_strings.append("{jobid},{pieceid},{cur_sheet},"
                                         "{total_sheet},{time},"
                                         "{result},{op}".format(jobid=job_string, pieceid=str(i).zfill(6),
                                                                cur_sheet=str(t).zfill(2),
                                                                total_sheet=str(num_sheets[i - 1])
                                                                .zfill(2), time=self.curr_feed_time,
                                                                result='0', op=ops))
                    self.curr_feed_time = self.add_seconds(self.curr_feed_time, 1)
                else:
                    sheet_strings.append("{jobid}{pieceid}{cur_sheet}{total_sheet}".format(jobid=job_string,
                                                                                           pieceid=str(i).zfill(6),
                                                                                           cur_sheet=str(t).zfill(2),
                                                                                           total_sheet=str
                                                                                           (num_sheets[i - 1])
                                                                                           .zfill(2)))
        filename = path.join(out_path, "feed_" + job_string + ".txt")
        with open(filename, 'w') as fp:
            fp.write(out_str.join(sheet_strings) + '\n')
        fp.close()
        self.curr_feed_time = None

    def gen_exit_data(self, create_damages=0, ops=None):
        out_str = "\n"
        repr_str = "\n"
        out_path = folder_construct(self.template_name)[2]
        piece_strings = []
        reprint_strings = []
        job_string = self.site_prefix + str(self.current_jobid).zfill(7)
        dc = 0
        current_damages = 0
        self.curr_exit_time = self.creation[1]

        if create_damages:
            dc = randint(5, 20)

        for i in range(1, self.current_piececount + 1):
            if create_damages:
                if 5 <= randint(1, 10) and current_damages <= dc:
                    current_damages += 1
                    if self.icd_mode:
                        piece_strings.append("{jobid},{pieceid},"
                                             "{time},{result},{op}".format(jobid=job_string, pieceid=str(i).zfill(6),
                                                                           time=self.curr_exit_time, result='1', op=ops))
                        reprint_strings.append("{jobid},{pieceid},"
                                               "{time},{result},{op}".format(jobid=job_string, pieceid=str(i).zfill(6),
                                                                             time=self.curr_exit_time, result='0', op=ops))
                        self.curr_exit_time = self.add_seconds(self.curr_exit_time, 1)
                    else:
                        reprint_strings.append("{jobid}{pieceid}".format(jobid=job_string, pieceid=str(i).zfill(6)))
                else:
                    if self.icd_mode:
                        piece_strings.append("{jobid},{pieceid},"
                                             "{time},{result},{op}".format(jobid=job_string, pieceid=str(i).zfill(6),
                                                                           time=self.curr_exit_time, result='0', op=ops))
                        self.curr_exit_time = self.add_seconds(self.curr_exit_time, 1)
                    else:
                        piece_strings.append("{jobid}{pieceid}".format(jobid=job_string, pieceid=str(i).zfill(6)))
            else:
                if self.icd_mode:
                    piece_strings.append("{jobid},{pieceid},"
                                         "{time},{result},{op}".format(jobid=job_string, pieceid=str(i).zfill(6),
                                                                       time=self.curr_exit_time, result='0', op=ops))
                    self.curr_exit_time = self.add_seconds(self.curr_exit_time, 1)
                else:
                    piece_strings.append("{jobid}{pieceid}".format(jobid=job_string, pieceid=str(i).zfill(6)))

        if create_damages:
            reprint_filename = path.join(out_path, "reprint_" + job_string + ".txt")
            with open(reprint_filename, 'w') as fp:
                fp.write(repr_str.join(reprint_strings) + '\n')
            fp.close()

        filename = path.join(out_path, "exit_" + job_string + ".txt")
        with open(filename, 'w') as fp:
            fp.write(out_str.join(piece_strings) + '\n')
        fp.close()
        self.curr_exit_time = None

    def __repr__(self):
        return "<BaseJIF(template_name='%s', piece_level='%s', num_jifs='%s')>" % \
               (self.template_name, self.piece_level, self.num_jifs)

