#!/usr/bin/env python

import Image

data = [ '%c%c%c%c' % (r, g, 0, 255) for r in range(0, 256) \
                                     for g in range(0, 256) ]
s = ''.join(data)
b = bytearray(s)
img = Image.frombuffer('RGBA', (256, 256), b)
img.save('test.png', 'PNG')
