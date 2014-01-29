#!/usr/bin/python
# Programma che usa la libreria MyOpen per andare in modalita monitor
# attende comando dal gateway
# lo scrive nel database sqlite
# utilizza il db per leggere l'ultimo stato
# e registrare se e cambiato

import MyOpen
import sys
import os


abs_dir=os.path.dirname(os.path.realpath(__file__))

if abs_dir[-4:] == "/lib":
    abs_dir=abs_dir[:-4]

#leggi impostazioni da config e le mette in un dizionario
conf=MyOpen.ReadConfig(abs_dir+"/config/config.cfg","MyMonitor").read()

#Connessione al gataway
gateway=MyOpen.Gateway(conf["gateway"],int(conf["port"]),"monitor")

#connessione al database
database=MyOpen.Db(abs_dir+"/log/"+conf["nomedb"])

#connessione al parser
parser=MyOpen.Parser(mydir=abs_dir)

while True:
    try:
        #leggo un codice dal gateway
        readcod=gateway.readcmd()

        #faccio il parsing
        par=parser.parsing(readcod)
        
        #verifico se e da saltare
        skipcod=parser.skipdouble("skip",readcod)
        
        #devo verificare se e' uguale all'ultima registrazione
        #se non vi e connessione al db lo salto
        #vuol dire che c'e' stata una richiesta di stato
        doublecod=False
        #se codice inizia come definito nel file di config skipdouble.cfg
        if parser.skipdouble("double",readcod):
            oldcod=database.lastrow(parser.who,parser.where)
            if type(oldcod)==dict:
                if readcod==oldcod["COD"]:
                    doublecod=True

        #scrivi nel db 
        if True:
            if not (skipcod and not conf["writedbskip"]):
                if not doublecod or conf["dbdouble"]:
                    lastid=database.addrow(parser.who,parser.where,readcod)
                    #print readcod 

    except KeyboardInterrupt:
        #premuto ctrl-c
        self.sys.exit("MyDaemon terminato su richiesta dell'utente")
    except Exception, e:
        self.sys.exit("Errore: "+str(e))




