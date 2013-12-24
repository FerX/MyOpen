#!/usr/bin/python

#script da sistemare con lettura impostazioni da file config

import MyOpen
import sys

print "ricorda di passare comando myopen racchiuso tra virgolette"

X=MyOpen.Gateway("192.168.1.13",20000)

if len(sys.argv)>1:
    cmd=sys.argv[1]
    print cmd
    print X.sendcmd(cmd)

