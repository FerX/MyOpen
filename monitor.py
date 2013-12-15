#!/usr/bin/python

from MyOpen import MyOpen
from time import time
S=MyOpen("192.168.1.13",20000,"monitor")

n=1
print "Litening:..."
while True:
    print n, S.readcmd()
    n+=1

