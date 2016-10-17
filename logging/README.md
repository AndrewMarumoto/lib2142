# API
```python
"""
Writes `data` to `logfile`.

Log files are stored in `(Battlefield 2142 server directory)/python/lib2142/logging/logs/`

If `header` is specified, `data` is indented under `header`.
ex.
  log('example data', header='[lib2142:example]')
  
  ...
  [lib2142:example]
    example data
  ...
"""
def log(data, header='', logfile='default.log'): None
```

```python
"""
Clears the specified log file.
Returns False on error (file does not exist, permissions, etc.)
"""
def clear_log(logfile): Bool
```

# Example
```python
from lib2142 import logging

# alias log function to specify header and logfile for all logging done in this module
def log(data): logging.log(data, header='[lib2142:example'], logfile='example.log')

# save chat messages
def onChatMessage(self, playerId, text, channel, flags):
  log('Player ID [%d]: %s\n' % (playerId, text))
```
