#!/usr/bin/python

import MyOpen
from time import time
S=MyOpen.Gateway("192.168.1.7",20000,"monitor")

n=1
print "Litening:..."
par=MyOpen.Parser()
while True:
    x=S.readcmd()
    print x,
    print par.parsing(x)
