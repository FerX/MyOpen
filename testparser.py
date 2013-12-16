#!/usr/bin/python

#test libreria per parsing codice myopen
import MyOpen
scenario=[]
#attivazione scenario
scenario.append("*0*12*22##")
#disattiva scenario
scenario.append("*0*12#0*22##")
#inizio programmazione scenario
scenario.append("*0*40#12*22##")
#fine programmazione scenario
scenario.append("*0*41#12*22##")
#cancella tutti gli scenari
scenario.append("*0*42*22##")


for a in scenario:
    x=MyOpen.Parser(a)
    print "Codice: "+x.COD
    print "Who: "+x.who,
    print " Who Human: "+x.who_human,
    print " Flag Who: "+str(x.who_flag)
    print "What: "+x.what,
    print " What Human: "+x.what_human,
    print " What flag: "+str(x.what_flag)
    print "Where: "+x.where,
    print " Where Human: "+x.where_human
    print "#"*30

