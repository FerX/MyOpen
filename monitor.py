#!/usr/bin/python

from MyOpen import MyOpen
from time import time
S=MyOpen("192.168.1.13",20000)

if S.connect("monitor"):
    n=1
    print "Litening:..."
    while True:
        print n, S.readcmd()
        n+=1
else:
    print "errore di connessione"

