#!/usr/bin/python

######################################################################
### Libreria MyOpen ### Connessione a gateway MyOpenWebNet Bticino ###
######################################################################
# Autore: Fernando Figaroli - FerX
# email: fernandofigaroli@gmail.com
# mi trovi su Google+
# Licenza: GPL 
# le donazioni sono ben accette PayPal fernando@figaroli.it
"""
La libreria MyOpen e' composta da una serie di classi ad oggetti
per interagire con un impianto domotico Bticino-Legrant che utilizza
il codice OpenWebNet per comunicare con i vari dispositivi.

class Gateway
    gestisce la connessione con il gataway per l'invio di comandi
    e l'ascolto in modalita monitor

class Db
    gestisce il database sqlite in cui tiene memorizzato il log

class Parser
    si occupa di riconoscere il codice OpenWebNet e renderlo
    piu' umano alla vista della persona

class Robot
    si occupa di gestire scenari semplici o super-complessi
    
class Notice
    si occupa di notificare via email, sms o altro un particolare messaggio.
    in futuro puo gestire anche la ricezione di comandi via sms o email.

il file config.cfg contiene le configurazioni di base della libreria
nella cartella config sono contenute le configurazioni personalizzabili
in base al proprio gusto e lingua.

###############################################################
# Autore: Fernando Figaroli - FerX
# email: fernandofigaroli@gmail.com
# mi trovi su Google+
# Licenza: GPL 
# le donazioni sono ben accette PayPal fernando@figaroli.it
###############################################################
"""

class Gateway:
    """
    Gestisce la connessione con il gataway per l'invio di comandi
    e l'ascolto in modalita' monitor
    uso:
    gate=MyOpen.Gateway(IP,PORT)    #crea connessione al gateway
    gate.sendcmd(CodiceOpenWebNet)  #invia comando e ritorna risposta
    gate.readcmd()                  #legge dal bus 
    gate.close()                    #chiude connessione
    
    gate=MyOpen.Gateway(IP,PORT,"monitor") #connessione in monitor
    es. stampare a monitor tutto il bus
    while True:
        print gate.readcmd()
    """
    import sys

    ACK="*#*1##" #OK
    NACK="*#*0##" #ERROR
    MONITOR="*99*1##" 
    COMMAND="*99*0##" 

    def __init__(self,gateway,port,tipo=""):
        """definisco variabili principali per le connessioni al gateway
        se richiesto entro in modalita monitor"""
        self.gateway=gateway
        self.port=port
        self.tipoconnessione=tipo
        if tipo=="monitor":
            self.__connect()

    def __connect(self):
        """self.__connect() 
                effettua una connesione socket al gateway MyOpenWebNet
        """             
        import socket
        try:
            self.Soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.Soc.connect((self.gateway,self.port))
        except:
            self.__errore("Errore di connessione al gateway, verifica IP, porta e se accesso concesso senza password")
        
        if self.tipoconnessione=="monitor":
            self.Soc.send(self.MONITOR)
        else:
            self.Soc.send(self.COMMAND)
        #il gateway deve rispondere ACK ACK
        a1=self.readcmd() 
        a2=self.readcmd()
        if not a1==a2==self.ACK:
            self.__errore("errore connessione... il gateway ha rispost: %s %s " % (a1,a2))
        return True 
        
    def close(self):
        """self.close()
                chiude la connessione socket al gateway se aperta
        """        
        if self.Soc: 
            self.Soc.close()
        return

    def sendcmd(self,cmd):
        """ self.send(str)
                invia il comando "str" al gateway e aspetta la risposta
                str deve contenere un codice OpenWebNet valido (es. *1*1*77##)
        """        
        R=True

        self.__connect()
        try:
            self.Soc.send(cmd)
        except:    
            self.__errore("Non stato possibile inviare il comando al gateway")

        #segnali di fine msg:
        #ACK =tutto bene, nulla da dire
        #NACK = segnale inviato, ma non andato a buon fine
        #risposta ACK = segnale inviato, risposta alla domanda, chiusura risposta
        mycmd=[]
        num_nack=0
        while True:
            R=self.readcmd()

            if R==self.ACK: 
                if mycmd==[]: mycmd=True
                self.close()
                return mycmd
            elif R==self.NACK:
                self.close()
                return False
            else:
                mycmd.append(R) 

    def readcmd(self):
        """ self.readcmd()
                legge dalla connessione socket una riga di messaggio
                per leggere piu testo metterlo in ciclo loop
        """
        #implementare errori
        #ricevo un carattere alla volta
        mycmd=""
        while True:
            try:
                R=self.Soc.recv(1)
            except:
                self.__errore("non e stato possibile ricevere dal gateway")
            mycmd=mycmd+R
            #se fine comando "##" esco
            if mycmd[-2:]=="##":   
                return mycmd


    def __errore(self,msg):
        self.close()
        self.sys.exit(msg) 






class Db:
    """
    Si occupa di gestire il database sqlite con memorizzato il logging dei comandi
    uso:
    database=MyOpen.Db(nomedb)
        connessione al db sqlite, riceve come argomento il nome del file database
        se non esiste lo crea e genera la tabella log

    database.addrow(who,where,codice)
        aggiunta di una riga, ritorna ID nuovo record inserito 
            who=chi
            where=dove
            codice=codice OpenWebNet (es. *1*1*77##)
        
    database.delrow(ID)
        cancella riga

    database.readrow(ID)
        legge una riga
        ritorna un dizionario con tutti i campi:
        ID=codice univoco
        TIME=secondi dal 1970
        WHO=chi
        WHERE=dove
        COD=codice OpenWebNet

    database.lastrow(who,where)
        ricerca nel database l'ultimo comando 
        che riguarda chi e dove specificati.
        serve principalmente per capire se 
        ha cambiato lo stato o no
        ritorna un dizionaro come in readnow()

    database.close()
        chiude la connessione con il db
    """
    
    import sqlite3
    import time

    def __init__(self,nomedb):
        self.nomedb=nomedb
        self.connect=None

        try:
            self.connect=self.sqlite3.connect(self.nomedb)
        except self.sqlite3.Error, e:
            self.__errore(e.args[0])

        #Verifico se la tabella log e presente nel database
        self.cursor = self.connect.cursor()
        #cur.execute("DROP table if exists 'log'")
        self.cursor.execute("SELECT name from sqlite_master WHERE type='table' AND name='log'")
        #primo avvio, creo la tabella log
        #ID = campo univoco auto-generato
        #TIME = secondi dal 1970 campo numerico con 2 decimali
        #WHO
        #WHE
        #COD
        self.cursor.execute("CREATE TABLE if not exists log "+\
                "(ID INTEGER PRIMARY KEY, TIME TEXT, WHO TEXT, WHE TEXT, COD TEXT)")
        self.connect.commit()

    def addrow(self, who, whe, cod):
        #aggiungo record
        tempo=str(self.time.time())
        sql="INSERT into log (time,who,whe,cod) values ('"+tempo+"','"+who+"','"+whe+"','"+cod+"')"
        self.cursor.execute(sql)
        self.connect.commit()
        #torna il nuovo id
        return self.cursor.lastrowid

    def delrow(self, del_id):
        #cancello il record con del_id
        sql="DELETE FROM log WHERE ID='"+str(del_id)+"'"
        self.cursor.execute(sql)
        self.connect.commit()

    def readrow(self, read_id):
        #leggo una determinata riga
        sql="SELECT ID,TIME,WHO,WHE,COD FROM log WHERE ID='"+str(read_id)+"'"
        self.cursor.execute(sql)
        res=self.cursor.fetchone()
        dictres={"ID":res[0],"TIME":res[1],"WHO":res[2],"WHERE":res[3],"COD":res[4]}
        return dictres 

    def lastrow(self,who,whe):
        #ricerca l'ultimo comando con who e whe
        #ritorna un dizionario con ID TIME WHO WHERE COD
        sql="SELECT ID,TIME,WHO,WHE,COD FROM log WHERE WHO='"+str(who)+"' AND WHE='"+str(whe)+"' ORDER BY ID desc"
        self.cursor.execute(sql)
        res=self.cursor.fetchone()
        dictres={"ID":res[0],"TIME":res[1],"WHO":res[2],"WHERE":res[3],"COD":res[4]}
        return dictres 

    def close(self):
        if self.__connect:
            self.__connect.close()

    def __errore(self,msg):
        self.close()
        self.sys.exit(msg) 


class Parser:
    """
    Fa il parsing dei codici my-open
    uso:
    pars=MyOpen.Parser(codice_open)
    pars --> object
    pars.who
    etc---    
    """
    import ConfigParser
    import re
    import sys
    import copy

    def __init__(self):
        conf=self.ConfigParser.RawConfigParser()
        conf.read("config.cfg")
        self.config=conf.get("MyOpen","configdir")
        self.who=""
        self.what=""
        self.where=""
        
        #load lists regex
        self.sys.path.insert(0,self.config)
        import regex

        #assign lists regex to dictionary
        self.regex={"0":regex.W0,"1":regex.W1,"2":regex.W2,"3":regex.W3,"4":regex.W4,\
                "5":regex.W5,"7":regex.W7,"9":regex.W9,"13":regex.W13,"15":regex.W15,\
                "16":regex.W16,"17":regex.W17,"1001":regex.W1001,"1004":regex.W1004,"1013":regex.W1013}

    def __readHuman(self,fileconfig,section,key):
        fileconfig=self.config+"/"+fileconfig+".cfg"
        try:
            config=self.ConfigParser.RawConfigParser()
            config.read(fileconfig)
            human=config.get(section, key)
        except:
            human="Not Found"
        return human

    def parsing(self,cod):
        self.COD=cod
        self.__who()
        return self.__regex()
        
    def __who(self):
        self.who=self.COD.split('*')[1]

        if self.who[0]=="#":
            self.who=self.who[1:]
        
        #cercare who in archivio
        self.who_human=self.__readHuman("WHO","WHO",self.who)
        return 

    def __regex(self):
        
        #usando who vado a recuperare tutte le regex che lo riguardano
        #converto i * in X e tolgo gli ultimi due ##
        tempCOD=self.COD.replace("*","X").rstrip("##")
        #corrispondenza variabili
        dvar={"A":"what","B":"where","R":"device","T":"thermo","O":"ol","V":"valv"}
        for reg in self.regex[self.who]:
            pars=self.re.compile(reg[0])
            pars=pars.match(tempCOD)
            
            if pars:
                resdict=pars.groupdict()
                resdicth=self.copy.copy(resdict)
                for chiave in resdict.keys():

                    #se finisce con H da umanizzare
                    if chiave[-1]=="H":
                        #riscrivere piu leggibile la seguente righa
                        resdicth[chiave]=self.__readHuman(dvar[chiave[0]],self.who,resdict[chiave].replace("#","G"))

                    #se finisce con T - temperatura
                    if chiave[-1]=="T":
                        resdicth[chiave]=resdicth[chiave][1:3]+","+resdicth[chiave][3]
                    #se campo where
                    if chiave=="B1H": self.where=resdict[chiave]
                    #se campo what
                    if chiave=="A1H": self.what=resdict[chiave]

                return reg[1].format(**resdicth)


    def skip(self,cod):
        """ determina se il codice rientra nella lista da saltare 
        riceve come argomento un codice openwebnet
        la lista da saltare e' memorizzata nel file skip.cfg
        """
      
        skip=self.ConfigParser.RawConfigParser()
        fileskip=self.config+"/"+"skip.cfg"
        skip.read(fileskip)
        skip=skip.items("skip")
        
        for x in skip:
            #verifico se cod inizia con quando definito in skip.cfg
            if cod.startswith(x[1]):
                #trovato, quindi devo saltare
                return True

