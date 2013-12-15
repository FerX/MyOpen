#!/usr/bin/python

######################################################################
### Libreria MyOpen ### Connessione a gateway MyOpenWebNet Bticino ###
######################################################################
# Autore: Fernando Figaroli - FerX
# email: fernandofigaroli@gmail.com
# mi trovi su Google+
# Licenza: GPL 
"""
Inserire qui una descrizione generica di tutta la libreria MyOpen

class MyOpenGateway
    si connette al gateway in modalita normale o monitor
    invia e riceve comandi

class MyOpenDB
    gestisce il database sqlite in cui tiene memorizzato il log
"""


class MyOpenGateway:
    """
    classe principale per la connessione al gateway
    
    """
    import sys

    ACK="*#*1##" #OK
    NACK="*#*0##" #ERROR
    MONITOR="*99*1##" 
    COMMAND="*99*0##" 

    def __init__(self,gateway,port):
        """definisco variabili principali per le connessioni al server"""
        self.gateway=gateway
        self.port=port

    def connect(self,tipo=""):
        """self.connect([tipo]) 
                effettua una connesione socket al gateway MyOpenWebNet
                uso: self.connect() - connessione normale per inviare comandi
                     self.connect("monitor") - connessione monitor, legge tutto lo stream
        """             
        import socket
        try:
            self.S=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.S.connect((self.gateway,self.port))
        except:
            self.errore("Errore di connessione al gateway, verifica IP, porta e se accesso concesso senza password")
        
        if tipo=="monitor":
            self.S.send(self.MONITOR)
        else:
            self.S.send(self.COMMAND)
        #il gateway deve rispondere ACK ACK
        a1=self.readcmd() 
        a2=self.readcmd()
        if not a1==a2==self.ACK:
            errore("errore connessione... il gateway ha rispost: %s %s " % (a1,a2))
        return True 
        
    def close(self):
        """self.close()
                chiude la connessione socket al gateway se aperta
        """        
        if self.S: 
            self.S.close()
        return

    def sendcmd(self,cmd):
        """ self.send(str)
                invia il comando "str" al gateway e aspetta la risposta
                str deve contenere un codice OpenWebNet valido (es. *1*1*77##)
        """        
        R=True

        self.connect()
        try:
            self.S.send(cmd)
        except:    
            errore("Non stato possibile inviare il comando al gateway")

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
                R=self.S.recv(1)
            except:
                self.errore("non e stato possibile ricevere dal gateway")
            mycmd=mycmd+R
            #se fine comando "##" esco
            if mycmd[-2:]=="##":   
                return mycmd


    def errore(self,msg):
        self.close()
        self.sys.exit(msg) 


class MyOpenDB:
    """
    Si occupa di gestire il database sqlite con memorizzato il logging dei comandi
    """
    import sqlite3

    def __init__(self,nomedb):
        """
        definisce le variabili generali del database e mi connetto
        """
        self.nomedb=nomedb
        self.connect=None

        try:
            self.connect=self.sqlite3.connect(self.nomedb)
        except self.sqlite3.Error, e:
            self.errore(e.args[0])

        #se nuovo file genero la-le tabelle necessarie
    
    def 

    def close(self):
        if self.connect:
            self.connect.close()

    def errore(self,msg):
        self.close()
        self.sys.exit(msg) 


