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

#leggi impostazioni da config e le mette in un dizionario
conf=MyOpen.ReadConfig("config.cfg","MyDaemon").read()

#Connessione al gataway
gateway=MyOpen.Gateway(conf["gateway"],int(conf["port"]),"monitor")

#connessione al database
if conf["writedb"]:
    database=MyOpen.Db(conf["nomedb"])

#connessione al parser
parser=MyOpen.Parser()

while True:
    #leggo un codice dal gateway
    readcod=gateway.readcmd()

    #verifico se e da saltare
    skipcod=parser.skip(readcod)
   
    #output a schermo se attivato
    if conf["screen"]:
        #continuo se non e da saltare
        if not (skipcod and conf["screenskip"]):
            par=parser.parsing(readcod)
            print readcod,par
    
    if conf["writedb"]:
        if not (skipcod and not conf["writedbskip"]):
            lastid=database.addrow(parser.who,parser.where,readcod)
            leggi=database.lastrow(parser.who,parser.where)
