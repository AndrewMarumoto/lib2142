"""
Collection of functions for debugging python scripts within 2142
- idodgebull3ts
"""

import sys

def runscript(script_data, g_vars=None, l_vars=None):
    if not g_vars:
        g_vars = {}

    output = {}
    if not 'PYDBG' in g_vars:
        g_vars['PYDBG'] = output

    try:
        exec(script_data, g_vars, l_vars)
    except:
        return (False, traceback())

    return (True, output)

def traceback():
    etype, evalue, etb = sys.exc_info()

    tmp = etb.tb_next
    while tmp is not None:
        etb = tmp
        tmp = tmp.tb_next

    lineno = etb.tb_lineno
    co = etb.tb_frame.f_code
    filename = co.co_filename
    name = co.co_name

    return 'File %s, line %d, in %s\n%s: %s' % (filename, lineno, name, etype, evalue)




