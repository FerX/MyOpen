#!/usr/bin/python

from MyOpen import MyOpen

S=MyOpen("192.168.1.13",20000)
S.connect("monitor")
while True:
        print S.readcmd()

        #ascolto in monitor

