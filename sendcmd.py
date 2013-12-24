#!/usr/bin/python

#script da sistemare con lettura impostazioni da file config

import MyOpen
import sys

X=MyOpen.Gateway("192.168.1.7",20000)

cmd=sys.argv[1]
print cmd
print X.sendcmd(cmd)

