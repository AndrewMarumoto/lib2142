"""
Interactive python interpreter though ingame commands
- idodgebull3ts
"""

import host
from lib2142.pydbg import traceback

from lib2142 import logging
def log(data): logging.log(data, header='[pydbg:ingame]')

def init():
    IngamePy()

class IngamePy:
    def __init__(self):
        self.result = {}
        self.g_vars = {'PYDBG': self.result,
                        'say': say}

        self.l_vars = {}
        host.registerHandler('ChatMessage', lambda *args: self.onChatMessage(*args), 1)


    def onChatMessage(self, playerId, text, channel, flags):
        text = text.replace("*\xa71DEAD\xa70*", '')
        text = text.replace("HUD_TEXT_CHAT_SQUAD", '')
        text = text.replace("HUD_TEXT_CHAT_TEAM", '')
        text = text.replace("HUD_CHAT_DEADPREFIX", '')

        if not text.startswith('!py '):
            return

        _, cmd = text.split(' ', 1)

        self.result.clear()
        try:
            exec(cmd, self.g_vars, self.l_vars)
        except:
            self.result['error:'] = traceback().split('\n')[-1]

        log('cmd: %s\nresult: %s' % (cmd, str(self.result)))

        if self.result:
            # console output in addition to server message
            host.rcon_feedback(playerId, str(self.result))
            say(str(self.result))


def say(msg):
    # 2142 doesn't like nested quotes, so switch out quotes entirely...
    msg = str(msg).replace('"', '!').replace("'", '|')
    host.rcon_invoke('game.sayall "[py] %s"' % (msg,))




