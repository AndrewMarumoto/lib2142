"""
Run/debug python scripts remotely
- idodgebull3ts
"""

import bf2
import socket
from lib2142 import logging
from lib2142 import microjson
from lib2142.pydbg import traceback, runscript


def log(data): logging.log(data, logfile='remote.log')

def init(host, port, interval=1):
    t = bf2.Timer(lambda _: check_for_data(host, port), interval, 1)
    t.setRecurring(interval)

def check_for_data(host, port):
    c = Conn(host, port)
    if not c.connect():
        return

    msg = c.readuntil()
    if msg is False:
        log('readuntil failed')
        return

    result = 'No result'
    try:
        if msg['op'] == 'runscript':
            (g_vars, l_vars), error = runscript(msg['data'])
            if error:
                log('runscript err:\n%s' % (error,))
                result = error
            elif 'PYDBG' in g_vars:
                result = g_vars['PYDBG']
            elif 'PYDBG' in l_vars:
                result = l_vars['PYDBG']
        else:
            result = 'Unsupported operation'

        c.write(result)
        c.close()
    except:
        log('check err:\n%s' % (traceback(),))


class Conn:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.buf = ''
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(2)
        try:
            self.sock.connect((self.host, self.port))
            return True
        except:
            self.sock = None
            return False

    def write(self, data):
        if not self.sock: return False

        data = '%s\n' % (microjson.to_json(data))

        try:
            self.sock.sendall(data)
            return True
        except:
            self.sock = None
            return False

    def readuntil(self, needle='\n'):
        if not self.sock: return False

        buf = ''
        while needle not in buf:
            try:
                buf += self.sock.recv(1)
            except:
                self.sock = None
                break

        buf = buf.strip()
        if buf:
            return microjson.from_json(buf)

        return False

    def close(self):
        if self.sock: self.sock.close()





