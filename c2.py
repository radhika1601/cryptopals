#!/usr/bin/python

def xor():
    a = raw_input('First num')
    b = raw_input('Second num')
    a = int(a, 16)
    b = int(b, 16)
    print(hex(a^b))

if __name__=='__main__':
    xor()
