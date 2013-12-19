#!/usr/bin/python
# Programma che usa la libreria MyOpen per andare in modalita monitor
# attende comando dal gateway
# se view lo stampa a video
# se db lo scrive nel database sqlite
# utilizza il db per leggere l'ultimo stato
# e registrare se e cambiato
import MyOpen
import ConfigParser
import time

#leggi impostazioni da config
conf=ConfigParser.RawConfigParser()
conf.read("config.cfg")
screen=conf.get("monitor","screen")
writedb=conf.get("monitor","writedb")
nomedb=conf.get("monitor","nomedb")

gateway=MyOpen.Gateway("192.168.1.7",20000,"monitor")
database=MyOpen.Db(nomedb)
print "In ascolto:..."
parser=MyOpen.Parser()
while True:
    x=gateway.readcmd()
    par=parser.parsing(x)
    print x,time.time(),
    print parser.who,parser.where,par
    lastid=database.addrow(str(time.time()),parser.who,parser.where,x)
    leggi=database.lastrow(parser.who,parser.where)
