import math
import ctypes
import struct

libc = ctypes.cdll.LoadLibrary('libc.so.6')
_mmap = libc.mmap
_mmap.restype = ctypes.c_ulong

def round_pagesize(size):
    return int(math.ceil(size / float(0x1000))) * 0x1000

def getaddr(x):
    return ctypes.addressof(x)

def getbuf(addr, size):
    return (ctypes.c_char*size).from_address(addr)

def alloc(size):
    size = round_pagesize(size)
    buf = _mmap(0, size, 7, 34, -1, 0)
    return getbuf(buf, size)

def mkbuf(x=0x1000):
    if type(x) is int:
        return alloc(x)
    elif type(x) is str:
        buf = alloc(len(x))
        buf[:len(x)] = x
        return buf

def patch(addr, new_code, orig_perms=5):
    buf = getbuf(addr, len(new_code))
    size = round_pagesize(len(new_code))

    libc.mprotect(addr & -0x1000, size, 7)
    buf[:] = new_code
    libc.mprotect(addr & -0x1000, size, orig_perms)

    return True

