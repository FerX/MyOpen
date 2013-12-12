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
        setLight() - imposta una luce
        readLight() - legge lo stato
        ...
        ...
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

    def connect(self,monitor=0):
        import socket
        self.monitor=monitor
        self.S=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.S.connect((self.server,self.port))
        if self.monitor:
            self.send(self.MONITOR)
        else:
            self.send(self.COMMAND)
        #implementare errori
        return 
        
    def close(self):
        self.S.close()
        return

    def send(self,cmd):
        #implementare errori
        return self.S.send(cmd)

    def read(self):
        #implementare errori
#        self.S.settimeout(1)
        R=self.S.recv(150)
        #suddivido in base a ##
        R=R.replace(self.ACK,"ACK##")
        R=R.replace(self.NACK,"NACK##")
        R=R.split("##")

        return R





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
