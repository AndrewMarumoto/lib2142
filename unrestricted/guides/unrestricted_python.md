## Overview
Instructions for loading an unrestricted python interpreter into Battlefield 2142.

## Caveats
* The instructions provided here are for the 64 bit linux server, but the process should work with minor adjustments on 32 bit linux and on windows.
* In Battlefield 2142's custom python interpreter, if an exception is uncaught it will not crash the entire server (like it would in bf2 iirc).  Without additional modifications, this process will cause uncaught python exceptions to crash the entire server.
* There is an old blog post about doing this for bf2, but it's very brief and does it in a way that's not entirely correct.  This is meant to be a more detailed guide.

## Instructions
* First, make a backup of `(2142)/bin/amd-64/libdice_py.so`.  If you end up breaking 2142 in the following process, you'll be able to restore it to a working state from the backup.

### Building a new python interpreter
* 2142 uses an ancient version of python (2.3.4).  You can grab the source from here: [python-2.3.4 download](https://www.python.org/ftp/python/2.3.4/Python-2.3.4.tgz)
* Extract it with `tar -xf ./Python-2.3.4.tgz` and `cd` into the directory
* Run `./configure --enable-shared BASECFLAGS=-U_FORTIFY_SOURCE` and then `make`
* `--enable-shared` makes it generate a shared library which we'll need later
* `U_FORTIFY_SOURCE` is needed because otherwise it crashes during compilation due to a known bug

### Replacing 2142's python
* In the compilation directory you'll see a file called `libpython2.3.so`.  Copy this into `(2142)/bin/amd-64/` and rename it to `libdice_py.so`.
* This next part isn't strictly necessary, but centralizes everything and makes it easier to manage.
* Create a new folder in `(2142)/` called `pylib`
* From the compilation directory, copy the contents of `./Lib/` and `./build/lib.linux-x86_64-2.3/` into `(2142)/pylib/`
* Now you need to point 2142's python to use the new libraries.  In `(2142)/python/bf2/__init__.py` add the following near the top of the file:
```python
  import sys
  sys.path = ['pylib/', 'python/', 'mods/bf2142/python/', 'admin/']
```
* If you didn't use `pylib/`, point `sys.path` at your equivalent.

### Adding new python modules
* Now that you've got an unrestricted python set up, you can start using some of the more fun/interesting python modules in your 2142 mods.
* The module that motivated me to go through this process in the first place is `ctypes`, so I'll show how to set that up here.  The process should generalize to whatever other modules you want to set up.
* Download the source from here: [ctypes download](http://downloads.sourceforge.net/project/ctypes/ctypes/1.0.2/ctypes-1.0.2.tar.gz)
* Extract it, etc.
* Run `LD_LIBRARY_PATH=/path/to/python-2.3.4-build-dir/ python-2.3.4 setup.py build`
* Of course, replace the placeholders with the actual paths to your python  comipilation directory and binary
* You can then copy the contents of `./build/lib.linux-x86_64-2.3/` into your `(2142)/pylib/` directory
* If you did everything correctly up to this point, you should be able to `import` and use your module from within 2142's python

If you're wondering how `ctypes` could be useful, see this [dynamically hooking game engine events](./game_engine_hooks/)
