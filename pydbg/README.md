# PyDbg
PyDbg consists of the main module which provides basic debugging functionality and, currently, two extensions to support remotely running python files and to support an interactive python interpreter through ingame commands.

# Main
The `traceback` module is broken in 2142's python, so the `pydbg.traceback` function provides a means to obtain a basic exception trace.

```python
from lib2142.pydbg import traceback

def some_function():
  try:
    # something that causes an exception
    'foo'.bar
  except:
    return traceback()
    
"""
...
File <string>, line 2, in <module>
<type 'exceptions.AttributeError'>: 'str' object has no attribute 'bar'
...
"""
```

The `pydbg.runscript` function provides a way to dynamically run a python script in 2142's context.

```python
from lib2142 import logging
from lib2142.pydbg import runscript

def init():
  testfile = open('test_file.py', 'r').read()
  success, output = runscript(testfile)
  if success:
    logging.log('testfile success:\n%s' % str(output))
  else:
    logging.log('testfile failed:\n%s' % str(output))
```

To send data to `output` from within your script, add an entry to the global `PYDBG` dictionary.
```python
def do_stuff():
  my_data = ...
  PYDBG['do_stuff result'] = my_data
```

# Remote
The `remote.py` script can be loaded by calling its `init` function with the host and port of the remote endpoint.
```python
from lib2142.pydbg import remote
remote.init('localhost', 1234)
```

`remote.py` will create a timer which will periodically trigger and check for updates from the remote endpoint.  If there is an update, it will process it and return the result.

To run a python file using this method, `util/runscript.py` is provided.  The HOST and PORT global variables must be configured to match those used by `remote.init()`.  Once those are set, it can be used by running:
```bash
python util/runscript.py [filename]
```

When the script exits, either the contents of the PYDBG global or an exception trace will be printed.

# Ingame
Note: this is currently set up for debugging purposes only.  Anyone on the server can execute commands.  Do not run this on a live server.

The ingame console can be loaded by running its `init` function.
```python
from lib2142.pydbg import ingame
ingame.init()
```

When ingame, players can run python code by sending `!py [command]` to chat.

A function is provided for sending messages to server chat.  Players can send `!py say('<message>')` to print data to server chat.

If the PYDBG global is modified or an exception is raised, its contents will be printed to the console of the player as well as to the server chat.  



