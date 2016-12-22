## Overview
This is a proof of concept for hooking events that are normally inaccessible from python.  It assumes you've set up [an unrestricted python interpreter for 2142](../unrestricted_python.md) and installed `ctypes`.  The hooking is done dynamically through python, rather than by statically modifying the executable.

## Caveats
* The code here is for 64 bit systems, it will not work as is on 32 bit
* The offsets may be different depending on which 2142 patch you're working with
* If you want to add new events, you'll need to reverse engineer the relevant parts of the server to find the offsets
* You'll also need to be able to write assembly

## Example: hooking comm rose events
So we want to get some python code executed whenever the user selects an option in the comm rose.  This might not be the best example, since iirc there's a thread on bfeditor.org about doing this in bf2 by modifying the HUD files to trigger a python remotecommand event or something.  But afaik there's no way to do it purely through python, so it should work fine to exemplify the process for hooking events.

### Reversing the RadioMessage event
I'm not going to go too in depth here, and will mostly just be stating my findings, but if you want to know more about the process of reversing you can contact me about it.

Anyway, the `handleRadioMessageReceivedEvent` function seemed like a good place to insert the hook (the linux builds of the server are compiled with debug symbols).  The second argument to this function is a pointer to a `RadioMessageReceivedEvent` class instance.  The byte at offset `0x28` in this class contains the player ID, and the byte at offset `0x2a` contains the selection ID.

The primary selection IDs are as follows.  There's a few more that I was too lazy to find, but that would be trivial to do.
```
0xd0 : Roger
0xd1 : Negative
0xd2 : Thanks
0xd3 : Sorry
0xdb : Spot
0xe4 : Medic
0xe5 : Backup
0xe7 : Ammo
0xec : Go, go, go!
0xef : Follow
```

### Hooking the RadioMessage event
When `handleRadioMessageReceivedEvent` gets called, we want our code to run first.  The general idea is that we're going to allocate some memory, write our hook code to it, and then overwrite the first few instructions of the above function with a `jmp` into our hooking code.  Once our code is done, it will run whatever instructions were overwritten and then jump back into the function.

#### Patching with ctypes
The `handleRadioMessageReceivedEvent` function begins with the following instructions.
```assembly
mov [rsp-0x20], rbp
mov [rsp-0x18], r12
mov rbp, rsi
mov [rsp-0x28], rbx
```

We want to patch the function to look like this.
```assembly
mov rax, <address of our code>
jmp rax
; <extra byte or two>
mov [rsp-0x28], rbx
```
So when this function is called, instead of normal operation it will first jump into our code before continuing through its normal path.

To do this with `ctypes`, we first want to get a reference to the memory where the function is located.  The following function will return a python object that can be used to read from and write to an arbitrary address.  It's basically a mutable string object.
```python
def getbuf(addr, size):
    return (ctypes.c_char*size).from_address(addr)
```

Before we can use this to patch in the jump though, we need to change the permission for the page where the function is mapped.  Normally this page is mapped `r-x`, so a write to it will cause a segfault.
```python
libc = ctypes.cdll.LoadLibrary('libc.so.6')
libc.mprotect(addr & -0x1000, size, 7) # change permissions to rwx
# < write patch here >
libc.mprotect(addr & -0x1000, size, 5) # restore original permissions
```
#### Setting up our hook
When a `RadioMessage` event occurs, it will first jump to our hook code.  The first thing we need to do is save register state.  This can be as simple as pushing all the relevant registers onto the stack (perhaps a more robust method would be using `getcontext` and `setcontext`).

Once that's done, we can do whatever we want here.

Once our hook is finished, we need to restore the register state.  Pop off the registers that were pushed earlier, or use `setcontext`.  Then execute whichever instructions were overwritten with the original jump. Finally jump back into the function at the next instruction after the overwritten ones.

Basically, it will look something like this.
```assembly
; <save register state>

; your code goes here

; <restore register state>

; run instructions that were overwritten with the original jmp
mov [rsp-0x20], rbp
mov [rsp-0x18], r12
mov rbp, rsi

; jump back to hooked function
mov rax, 0x45762d
jmp rax
```

This code then needs to be mapped into memory.  `mmap` via `ctypes` is probably the best way to do this.  Once it's mapped, we can change the placeholder bytes in the `jmp` patch to point to it.

#### Calling back to python
So we've got assembly code executing for the event.  But we wanted python.

There are a couple ways to do this, but I'm going to show the easy way for now (which is probably also the less correct way, but it works well enough).  The 2142 server imports a bunch of functions from the python library, one of which is `PyRun_SimpleString`.  This function takes one argument, a string, and runs it as python code.

```assembly
lea rdi, [rip+cmd] ; load address of cmd string into rdi (first argument to function call)
mov rax, 0x407d60 ; address of PyRun_SimpleString import
call rax

cmd:
db "import host; host.rcon_invoke('game.sayall test')",0
```

#### Passing arguments
Now we've got python executing for the event, but we still don't know which player triggered it or which selection they made.  Again, there are several ways of doing this.  For now, I just have the assembly code writing whatever values are needed to a constant offset in the mapped page and then call back into a python function that will extract that values and propagate the event.

```assembly
lea rax, [rip] ; get address of instruction
and rax, -0x1000 ; get page-aligned address
mov [rax+0xf00], rsi ; save rsi to offset 0xf00 in page
                     ; (rsi is pointing to a RadioMessageReceivedEvent class instance)
```

