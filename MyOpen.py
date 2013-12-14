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
            self.connect()

    def connect(self):
        """self.connect([tipo]) 
                effettua una connesione socket al gateway MyOpenWebNet
                uso: self.connect() - connessione normale per inviare comandi
        """             
        import socket
        try:
            self.Soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.Soc.connect((self.gateway,self.port))
        except:
            self.errore("Errore di connessione al gateway, verifica IP, porta e se accesso concesso senza password")
        
        if self.tipoconnessione=="monitor":
            self.Soc.send(self.MONITOR)
        else:
            self.Soc.send(self.COMMAND)
        #il gateway deve rispondere ACK ACK
        a1=self.readcmd() 
        a2=self.readcmd()
        if not a1==a2==self.ACK:
            errore("errore connessione... il gateway ha rispost: %s %s " % (a1,a2))
        return True 
        
    def close(self):
        """self.close()
                chiude la connessione socket al gateway
        """        
        self.Soc.close()
        return

    def sendcmd(self,cmd):
        """ self.send(str)
                invia il comando "str" al gateway e aspetta la risposta
                str deve contenere un codice OpenWebNet valido (es. *1*1*77##)
        """        
        R=True

        self.connect()
        try:
            self.Soc.send(cmd)
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
                R=self.Soc.recv(1)
            except:
                self.errore("non e stato possibile ricevere dal gateway")
            mycmd=mycmd+R
            #se fine comando "##" esco
            if mycmd[-2:]=="##":   
                return mycmd


    def errore(self,msg):
        print self
        self.close()
        self.sys.exit() 


