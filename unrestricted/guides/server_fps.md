## Overview
By default, the server fps is locked at 36.  Changing it to significantly higher values results in some instability, but it appears to be fine up to around 100 fps at least.

## Reversing
The code relating to the server fps can be found near the end of the `dice::hfe::BF2Engine::mainLoop` function.  In C++, the code would look something like the following (simplified):
```C++
double delay = server_fps - elapsed_time;
while (delay > 0.0)
{
  double start = dice::hfe::g_system::getWallClockTime();
  dice::hfe::g_system::sleep(delay);
  delay = delay - dice::hfe::g_system::getWallClockTime() - start;
}
```

As you can see, `delay` is calculated from the `server_fps` value minus the elapsed time for the current tick.  The loop just ensures that it sleeps the full amount.

The `server_fps` variable is global.  By default, it's equal to `2/60` or `0.03333`.

## Changing the server fps
As `server_fps` is global, all we need to do is change the value at its address to our desired value.  Let's say we want to double the default fps.  To format the value correctly, we can do
```python
value = struct.pack('<d', 1/60.)
```

On my test server (linux x64), `server_fps` is at `0xb165b0`.  This can be done statically, but it's much cleaner to do it dynamically through python with ctypes.

```python
import struct
from lib2142.util import *
patch(0xb165b0, struct.pack('<d', 1/60.))
```
