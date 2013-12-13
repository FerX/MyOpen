#!/usr/bin/python

######################################################################
### Libreria MyOpen ### Connessione a gateway MyOpenWebNet Bticino ###
######################################################################
# Autore: Fernando Figaroli - FerX
# email: fernandofigaroli@gmail.com
# mi trovi su Google+
# Licenza: GPL 
# Credits: Ho preso idee dal progetto pymyhome di Flavio Giovannangeli

class MyOpen:
    """
    classe principale per la connessione al gateway
    
    metodi:
        connect() - apre la connessione
        close() - chiude la connessione
        ...da sviluppare ...
    
    """
    #Classificazione dei messaggi OPEN
    #ACK *#*1##
    #NACK *#*0##
    #NORMALE *CHI*COSA*DOVE##
    #RICHIESTA STATO *#CHI*DOVE##
    #RICHIESTA GRANDEZZA *#CHI*DOVE*GRANDEZZA##
    #STRITTURA GRANDEZZA *#CHI*DOVE*#GRANDEZZA*VAL1*VAL2*VALN##

    ACK="*#*1##" #OK
    NACK="*#*0##" #ERROR
    MONITOR="*99*1##" 
    COMMAND="*99*0##" 


    def __init__(self,server,port):
        """definisco variabili principali per le connessioni al server"""
        self.server=server
        self.port=port

    def connect(self,tipo=""):
        """self.connect([tipo]) 
                effettua una connesione socket al gateway MyOpenWebNet
                uso: self.connect() - connessione normale per inviare comandi
                     self.connect("monitor") - connessione monitor, legge tutto lo stream
        """             
        import socket
        self.S=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.S.connect((self.server,self.port))
        if tipo=="monitor":
            self.S.send(self.MONITOR)
        else:
            self.S.send(self.COMMAND)
            a1=self.readcmd() #ritorna TRUE se ACK
            a2=self.readcmd() #ritorna TRUE se ACK
            if not a1==a2==self.ACK:
                print "errore connessione... parte da sistemare con try: "

        #implementare errori
        return True 
        
    def close(self):
        """self.close()
                chiude la connessione socket al gateway
        """        
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
            R=False
        #compongo la risposta

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
            R=self.S.recv(1)
            mycmd=mycmd+R
            #se fine comando "##" esco
            if mycmd[-2:]=="##":   
                return mycmd





###############
### TESTING
###############
#import time
#casa=MyOpen("192.168.1.7",20000)
#casa.connect()
#print "connesso... leggo cosa risponde"
#print casa.read()
#
#print "accendo luce scala"
#casa.send("*1*0*77##")
#print "interrogo stato luce scala"
#casa.send("*#1*77##")
#print "leggo.."
#print casa.read()
#
##print "attendo 1 secondo"
##time.sleep(1)
##print "spengo luce scala"
##print casa.send("*1*0*77##")
##print "interrogo stato luce scala"
##print casa.send("*#1*77##")
##print casa.read()
##
##time.sleep(1)
#print "vado in modalita monitor.."
#casa.close()
#casa.connect(monitor=1)
#while True:
#    print casa.read()
#
#
