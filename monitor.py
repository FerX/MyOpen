#!/usr/bin/python
# Programma che usa la libreria MyOpen per andare in modalita monitor
# attende comando dal gateway
# se view lo stampa a video
# se db lo scrive nel database sqlite
# utilizza il db per leggere l'ultimo stato
# e registrare se e cambiato
import MyOpen
from time import time

view=True
db=True
dbfile="monitor.db"

gateway=MyOpen.Gateway("192.168.1.7",20000,"monitor")
database=MyOpen.Db(dbfile)
n=1
print "In ascolto:..."
parser=MyOpen.Parser()
while True:
    x=gateway.readcmd()
    print x,
    print parser.parsing(x)
