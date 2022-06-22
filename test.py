from msilib.schema import Binary

import struct

def rawbytes(s):
    """Convert a string to raw bytes without encoding"""
    outlist = []
    for cp in s:
        num = ord(cp)
        if num < 255:
            outlist.append(struct.pack('B', num))
        elif num < 65535:
            outlist.append(struct.pack('>H', num))
        else:
            b = (num & 0xFF0000) >> 16
            H = num & 0xFFFF
            outlist.append(struct.pack('>bH', b, H))
    return b''.join(outlist)

name = 'Philipp_Mi\xc3\x9ffelder'

nameB = rawbytes(name)
print(nameB)
print(nameB.decode('utf-8'))



name2 = b'Semir_\xc5\xa0tili\xc4\x87'
print(name2.decode('utf-8'))
