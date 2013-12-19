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
    print cpars.parsing(a)


auto=[]
auto.append("*2*0*12##")
auto.append("*2*1*2##")
auto.append("*2*2*#1##")
cpars=MyOpen.Parser()
print "Test auto"
for a in auto:
    print "Codice: "+a,
    print cpars.parsing(a)


auto=[]
auto.append("*#13**0*10*12*12*101##")
auto.append("*#13**1*03*12*12*2013##")
auto.append("*#13**10*192*168*1*13##")
auto.append("*#13**11*255*255*255*0##")
auto.append("*#13**12*00*255*10*10*10*1##")
auto.append("*#13**15*4##")
auto.append("*#13**16*4122*234*5543##")
cpars=MyOpen.Parser()
print "Test 13"
for a in auto:
    print "Codice: "+a,
    print cpars.parsing(a)


auto=[]
auto.append("*#4*1*0*0205##")
auto.append("*#4*301*0*0275##")
auto.append("*#4*2*12*0375*3##")
auto.append("*#4*2*13*01##")
auto.append("*#4*3*14*0501*3##")
auto.append("*#4*3*19*3*5##")
auto.append("*#4*102*4##")
auto.append("*#4*24*#0##")
cpars=MyOpen.Parser()
print "Test 4 termo"
for a in auto:
    print "Codice: "+a,
    print cpars.parsing(a)


auto=[]
auto.append("*5*11*#6##")
auto.append("*5*6**##")
auto.append("*5*18*#3##")
auto.append("*5*8**##")
auto.append("*5*15*#2##")
cpars=MyOpen.Parser()
print "Test 5 Antifurto"
for a in auto:
    print "Codice: "+a,
    print cpars.parsing(a)
    
