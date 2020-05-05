#!/usr/bin/python
import sys

def hextoBase64():
    s = (sys.argv[1].decode('hex')).encode('base64')
    print(s)

hextoBase64()
