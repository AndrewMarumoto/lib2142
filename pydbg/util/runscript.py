"""
Run python files on a remote 2142 server
- idodgebull3ts
"""

import sys
import json
import pprint
import socket
import traceback

HOST = ''
PORT = 5557

def main(argc, argv):
    if argc != 2:
        print 'Usage: python %s filename' % argv[0]
        return

    filename = argv[1]

    try:
        with open('%s' % filename, 'rb') as f: f = f.read()
    except IOError:
        print 'Unable to open file "%s"' % filename
        return

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(5)
        s.bind((HOST, PORT))
        s.listen(1)

        conn, addr = s.accept()
        conn.settimeout(2)

        msg = {'op': 'runscript',
                'data': f}

        conn.sendall('%s\n' % json.dumps(msg))

        buf = ''
        while '\n' not in buf:
            try:
                buf += conn.recv(4096)
            except socket.timeout:
                print 'socket timeout'
                return
            except:
                return

        pprint.pprint(json.loads(buf.split('\n', 1)[0]))

    except:
        traceback.print_exc()

if __name__ == '__main__': main(len(sys.argv), sys.argv)


