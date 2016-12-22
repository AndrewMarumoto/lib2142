import host
import math
import ctypes
import struct
import traceback

libc = ctypes.cdll.LoadLibrary('libc.so.6')
mmap = libc.mmap
mmap.restype = ctypes.c_ulong

def round_pagesize(size):
    return int(math.ceil(size / float(0x1000))) * 0x1000

def getaddr(x):
    return ctypes.addressof(x)

def getbuf(addr, size):
    return (ctypes.c_char*size).from_address(addr)

def mkbuf(x=0x1000, rwx=False):
    if rwx:
        def alloc(size):
            size = round_pagesize(size)
            return getbuf(mmap(0, size, 7, 34, -1, 0), size)
    else:
        alloc = ctypes.create_string_buffer

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

def example_callback():
    if not hasattr(example_callback, 'buf'):
        return

    data = example_callback.buf[0xf00:]
    event = struct.unpack('<Q', data[:8])[0]
    event_data = getbuf(event, 0x50)

    opt = ord(event_data[0x2a:][:1])
    sender = ord(event_data[0x28:][:1])

    radio = {
            0xe5: 'backup',
            0xdf: 'pickup',
            0xd0: 'roger',
            0xd1: 'negative',
            0xd2: 'thanks',
            0xd3: 'sorry',
            0xe4: 'medic',
            0xe7: 'ammo',
            0xec: 'go',
            0xdb: 'spot',
            0xef: 'follow',
            }

    if opt in radio:
        selection = radio[opt]
    else:
        selection = str(opt)

    host.rcon_invoke('game.sayall %s_%d\n' % (selection, sender))

def example_hook():
    handle_radiomessage = 0x457620

    stub = '\x48\xB8\x41\x41\x41\x41\x41\x41\x41\x41\xFF\xe0'
    hook = "\x57\x56\x52\x53\x55\x41\x54\x41\x55\x41\x56\x48\x8D\x05\x00\x00\x00\x00\x48\x25\x00\xF0\xFF\xFF\x48\x89\xB0\x00\x0F\x00\x00\x48\x8D\x3D\x2A\x00\x00\x00\x48\xC7\xC0\x60\x7D\x40\x00\xFF\xD0\x41\x5E\x41\x5D\x41\x5C\x5D\x5B\x5A\x5E\x5F\x48\x89\x6C\x24\xE0\x4C\x89\x64\x24\xE8\x48\x89\xF5\x48\xC7\xC0\x2D\x76\x45\x00\xFF\xE0"

    cmd = 'from bf2 import dyn_patch; dyn_patch.example_callback();'

    hook_buf = mkbuf(hook+cmd, 1)
    example_callback.buf = hook_buf

    patch(handle_radiomessage, stub.replace('A'*8, struct.pack('<Q', getaddr(hook_buf))))

def init():
    try:
        example_hook()
    except:
        a = open('errors', 'wb')
        traceback.print_exc(file=a)
        a.close()


