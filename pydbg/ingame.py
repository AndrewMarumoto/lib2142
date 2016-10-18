"""
Interactive python interpreter though ingame commands
- idodgebull3ts
"""

import host
from lib2142.pydbg import runscript, traceback

from lib2142 import logging
def log(data): logging.log(data, header='[pydbg:ingame]')

def init(log_cmds=False):
    IngamePy(log_cmds)

class IngamePy:
    def __init__(self, log_cmds):
        self.log_cmds = log_cmds
        host.registerHandler('ChatMessage', lambda *args: self.onChatMessage(*args), 1)

    def onChatMessage(self, playerId, text, channel, flags):
        text = text.replace("*\xa71DEAD\xa70*", '')
        text = text.replace("HUD_TEXT_CHAT_SQUAD", '')
        text = text.replace("HUD_TEXT_CHAT_TEAM", '')
        text = text.replace("HUD_CHAT_DEADPREFIX", '')

        if not text.startswith('!py '):
            return

        _, cmd = text.split(' ', 1)

        (g_vars, l_vars), error = runscript(cmd, {'say': say})

        if self.log_cmds or error:
            res = ''
            if error:
                res = error.split('\n')[-1]
            elif 'PYDBG' in g_vars:
                res = g_vars['PYDBG']
            elif 'PYDBG' in l_vars:
                res = l_vars['PYDBG']

            if res:
                log('[%s]:\n%s' % (cmd, res))
                say(res)


def say(msg):
    # 2142 doesn't like nested quotes, so switch out quotes entirely...
    msg = str(msg).replace('"', '!').replace("'", '|')
    host.rcon_invoke('game.sayall "[py] %s"' % (msg,))




