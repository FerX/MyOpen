#!/usr/bin/python
#Programma semplice per inviare manualmente comandi OpenWebNet al gateway
#legge le impostazioni del gateway dal file di config.cfg
#esempio uso:
#./sendcmd.py "*1*1*77##"

from lib import MyOpen
import sys

#leggi impostazioni da config e le mette in un dizionario
conf=MyOpen.ReadConfig("config/config.cfg","MyDaemon").read()

#Connessione al gataway
gateway=MyOpen.Gateway(conf["gateway"],int(conf["port"]))

if len(sys.argv)==1:
    #nessun argomento passato
    print """sendcmd.py - programma per inviare comandi al gateway
             uso: ./sendcmd.py comandoOpenWebNet
             si possono passare anche piu comandi simultaneamente
             es: ./sendcmd.py *1*1*77## *1*1*76## """
    sys.exit()

for cmd in sys.argv[1:]:
    print "Invio: "+cmd
    print "Risposta: ",
    print gateway.sendcmd(cmd)

