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

    def connect(self,tipo="command"):
        """self.connect([tipo]) 
                effettua una connesione socket al gateway MyOpenWebNet
                uso: self.connect() - connessione normale per inviare comandi
                     self.connect("monitor") - connessione monitor, legge tutto lo stream
        """             
        import socket
        self.S=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.S.connect((self.server,self.port))
        if tipo=="monitor":
            self.send(self.MONITOR)
        else:
            self.send(self.COMMAND)
        #implementare errori
        return 
        
    def close(self):
        """self.close()
                chiude la connessione socket al gateway
        """        
        self.S.close()
        return

    def send(self,cmd):
        """ self.send(str)
                invia il comando "str" al gateway e aspetta la risposta
                str deve contenere un codice OpenWebNet valido (es. *1*1*77##)
        """        
        R=True
        try:
            by=self.S.send(cmd)
        except:    
            R=False
        n=0
        mycmd=""
        #compongo la risposta elimiando gli ACK
        #il terzo ACK senza la fine del messaggio
        while True:
            R=self.read()
            print X,n
            if R==self.ACK: 
                n+=1
                if n==3: 
                    break
            else:
                mycmd=mycmd+R
        return mycmd 

    def read(self):
        """ self.read()
                legge dalla connessione socket una riga di messaggio
                per leggere più testo metterlo in ciclo loop
        """
        #implementare errori
        #ricevo un carattere alla volta, ritorno quando ##
        n=0
        mycmd=""
        while True:
            R=self.S.recv(1)
            mycmd=mycmd+R
            if R=="#": n+=1
            if n==2: break 
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
