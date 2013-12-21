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
import sys

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
    try:
        #leggo un codice dal gateway
        readcod=gateway.readcmd()

        #faccio il parsing
        par=parser.parsing(readcod)
        
        #verifico se e da saltare
        skipcod=parser.skip(readcod)
        
        #devo verificare se e' uguale all'ultima registrazione
        #vuol dire che c'e' stata una richiesta di stato
        #non devo quindi memorizzarlo
        #solo se who=1 e ??? 
        doublecod=False
        if parser.who in ["1"]:
            oldcod=database.lastrow(parser.who,parser.where)
            if type(oldcod)==dict:
               if readcod==oldcod["COD"]:
                    doublecod=True

        #output a schermo se attivato
        if conf["screen"]:
            #continuo se non e da saltare
            if not skipcod or conf["screenskip"]:
                #continuo anche se e un duplicato
                if not doublecod or conf["screendouble"]:
                    print readcod,par
        
        #scrivi nel db 
        if conf["writedb"]:
            if not (skipcod and not conf["writedbskip"]):
                if not doublecod or conf["dbdouble"]:
                    lastid=database.addrow(parser.who,parser.where,readcod)
    
    except KeyboardInterrupt:
        #premuto ctrl-c
        sys.exit("MyDaemon terminato su richiesta dell'utente")
    except Exception, e:
        sys.exit("Errore: "+str(e))
