"""
Simple logging implementation
- idodgebull3ts
"""

import datetime

REMOTE_ADDR = ''
REMOTE_PORT = 0
LOG_REMOTE = False
LOG_PATH = './python/lib2142/logging/logs/'

def log(data, header='', logfile='default.log'):
    log_path = '%s/%s' % (LOG_PATH, logfile)

    # check if logfile already exists
    flags = 'a'
    try:
        open(log_path, 'r')
    except IOError:
        flags = 'w'

    try:
        f = open(log_path, flags)
    except IOError:
        # kinda screwed here
        return False

    timestamp = str(datetime.datetime.now())
    if header:
        f.write('[%s] %s\n%s\n' % (timestamp, header, indent(data)))
    else:
        f.write('[%s] %s\n' % (timestamp, data))

    f.close()

    if LOG_REMOTE:
        # TODO: set up logging to external server
        pass


def clear_log(logfile):
    log_path = '%s/%s' % (LOG_PATH, logfile)

    try:
        open(log_path, 'w')
        return True
    except IOError:
        return False


def indent(data):
    pad = '  '
    return pad + ('\n' + pad).join(data.split('\n'))

