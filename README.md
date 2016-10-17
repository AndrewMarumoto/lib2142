# About
This repository aims to fill in some of the gaps created by DICE's gutting of the python standard library and to provide useful 2142 specific functionality.  Some of the scripts are original, while others are existing modules for current versions of python that I ported to work with python 2.3.4 and within 2142's limitations.

The current state of the repository reflects the functionality that I've needed for the initial implementation of some basic mods.  I plan on updating this library with new functionality as I come across issues and create/port solutions.

# Installation
```bash
cd (Battlefield 2142 server directory)/python/
git clone https://github.com/AndrewMarumoto/lib2142.git
```

# Usage
If installed as above, lib2142 can be accessed from any python code running in the game by `import lib2142`

Usage information for specific modules can be found in their respective folders.

# Original modules
* [pydbg](./pydbg/)
* [logging](./logging/)
* [base64](./b64.py)

# Ported modules

* microjson - https://github.com/phensley/microjson
* StringIO (no modifications) - https://github.com/python-git/python/blob/master/Lib/StringIO.py