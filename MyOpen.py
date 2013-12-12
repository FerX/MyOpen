#!/usr/bin/python

######################################################################
### Libreria MyOpen ### Connessione a gateway MyOpenWebNet Bticino ###
######################################################################
# Autore: Fernando Figaroli - FerX
# email: fernandofigaroli@gmail.com
# mi trovi su Google+
#
# Licenza: GPL 
# Credits: Ho preso idee dal progetto pymyhome di Flavio Giovannangeli

class MyOpen:
    """
    classe principale per la connessione al gateway
    
    metodi:
        connect() - apre la connessione
        disconnect() - chiude la connessione
        setLight() - imposta una luce
        readLight() - legge lo stato
        ...
        ...
        ...da sviluppare ...
    """

    def __init__(self,server,port):
        """definisco variabili principali per le connessioni al server"""
        self.server=server
        self.port=port
    
    def connect(self):
        import socket
        try:
            self.S=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.S.connect((self.server,self.port))
        except Exception, e:
            self.S=None
        finally:
            return self.S
        
    def disconnect():
        pass

    def sendData(self,cmd):
        self.S.send(cmd)

    



###############
### TESTING
###############

casa=MyOpen("192.168.1.7",20000)
casa.connect()
casa.sendData("*1*0*77##")


