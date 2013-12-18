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
scenario.append("*0*42#*22##")
scenario.append("*0*43*22##")
scenario.append("*0*44*22##")
scenario.append("*0*45*22##")
scenario.append("*0*46*22##")

cpars=MyOpen.Parser()
print "Test scenario"
for a in scenario:
    print "Codice: "+a,
    x=cpars.parsing(a)



luci=[]
luci.append("*1*1*12##")
luci.append("*1*1*2##")
luci.append("*1*0*12##")
luci.append("*#1*3*1*50*120##")
luci.append("*1*8*13##")
luci.append("*1*23*13##")
luci.append("*#1*12*2*1*12*2##")
cpars=MyOpen.Parser()
print "Test Luci"
for a in luci:
    print "Codice: "+a,
    x=cpars.parsing(a)


auto=[]
auto.append("*2*0*12##")
auto.append("*2*1*2##")
auto.append("*2*2*#1##")
cpars=MyOpen.Parser()
print "Test auto"
for a in auto:
    print "Codice: "+a,
    x=cpars.parsing(a)
    
