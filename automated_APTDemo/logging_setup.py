import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

log_dir = os.path.join(BASE_DIR, 'logs')
log_file = os.path.join(log_dir, 'aptdemo.log')

master_logger = None


def init_logging():
    global master_logger
    if master_logger is None:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logging.basicConfig(filename='{}'.format(log_file),
                            level=logging.DEBUG,
                            format='[%(levelname)s] %(module)s-%(asctime)s: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        master_logger = logging.getLogger()
    return master_logger
