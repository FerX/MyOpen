#!/usr/bin/python

#test libreria per parsing codice myopen

import MyOpen
a=[]
a.append(MyOpen.Parser("*0*2*23##"))

a.append(MyOpen.Parser("*1*0*23##"))

a.append(MyOpen.Parser("*1*1*23##"))

a.append(MyOpen.Parser("*#1*2*1*23##"))

a.append(MyOpen.Parser("*2*1*23##"))

for x in a:
    print "Codice: "+x.COD
    print "Who: "+x.who
    print "Who Human: "+x.who_human
    print "Flag Who: "+str(x.who_flag)
    print "What: "+x.what
    print "What Human: "+x.what_human
    print "Where: "+x.where
    print "Where Human: "+x.where_human
    print "#"*30

