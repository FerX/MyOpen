#!/usr/bin/python
# Programma che usa la libreria MyOpen per andare in modalita monitor
# attende comando dal gateway
# lo scrive nel database sqlite
# utilizza il db per leggere l'ultimo stato
# e registrare se e cambiato

#importo libreria per rendere demone 
import logging
from daemons.base import Daemon

class Server(Daemon):
    from lib import MyOpen
    import sys
    
    def setdir(self,mydir):
        self.mydir=mydir

    def run(self):
        import os
        #leggi impostazioni da config e le mette in un dizionario
        conf=self.MyOpen.ReadConfig(self.mydir+"/config/config.cfg","MyDaemon").read()

        #Connessione al gataway
        gateway=self.MyOpen.Gateway(conf["gateway"],int(conf["port"]),"monitor")

        #connessione al database
        database=self.MyOpen.Db(self.mydir+"/log/"+conf["nomedb"])

        #connessione al parser
        parser=self.MyOpen.Parser(mydir=self.mydir)

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
   

            except KeyboardInterrupt:
                #premuto ctrl-c
                self.sys.exit("MyDaemon terminato su richiesta dell'utente")
            except Exception, e:
                self.sys.exit("Errore: "+str(e))


if __name__ == '__main__':
    import sys
    import os
    arg=sys.argv
    msg="""
    Utilizzo - ./MyDaemon.py [start] [stop] [restart]
    
    """
    
    if len(arg) == 1:
        sys.exit(msg)

    action = arg[1]
    
    #logging.basicConfig(filename="daemon.log", level=logging.DEBUG)
    logging.basicConfig( level=logging.ERROR)
    d = Server(pidfile='MyDaemon.pid')
    d.setdir(os.getcwd())

    if action == "start":
        print d.start()
    elif action == "stop":
        d.stop()
    elif action == "restart":
        d.restart()
    else:
        sys.exit(msg)

