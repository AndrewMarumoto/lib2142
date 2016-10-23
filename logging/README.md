# Example
```python
from lib2142 import logging

# alias log function to specify header and logfile for all logging done in this module
def log(data): logging.log(data, header='[lib2142:example'], logfile='example.log')

# save chat messages
def onChatMessage(self, playerId, text, channel, flags):
  log('Player ID [%d]: %s\n' % (playerId, text))
```
