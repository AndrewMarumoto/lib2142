"""
Shitty base64 implementation because 2142's is broken
- idodgebull3ts
"""


charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

def encode(data):
    npad = 3 - (len(data) % 3)
    if npad == 3: npad = 0
    data += '\0'*npad

    res = ''
    for i in range(0, len(data), 3):
        u = (ord(data[i]) << 16) | (ord(data[i+1]) << 8) | ord(data[i+2])
        res += charset[u >> 18]
        res += charset[(u >> 12) & 63]
        res += charset[(u >> 6) & 63]
        res += charset[u & 63]

    if npad:
        return res[:-npad] +  ('='*npad)
    else:
        return res


def decode(data):
    data = data.strip()
    npad = 0
    if data[-1] == '=':
        npad = 1
        if data[-2] == '=':
            npad = 2

    if npad:
        data = data[:-npad] + ('A'*npad)

    res = ''
    for i in range(0, len(data), 4):
        u = ((charset.index(data[i]) << 18) +
             (charset.index(data[i+1]) << 12) +
             (charset.index(data[i+2]) << 6) +
             (charset.index(data[i+3])))

        res += (chr((u >> 16) & 0xff) +
                chr((u >> 8) & 0xff) +
                chr(u & 0xff))

    if npad:
        return res[:-npad]
    else:
        return res



# aliases
encodestring = encode

