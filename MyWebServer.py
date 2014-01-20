#!/usr/bin/python 

import cherrypy

#importo il mio file dove definisco le var statiche
from lxml import etree
#import pickle
import urllib
from lib import MyOpen
from lib import MyWeb

#leggi impostazioni da config e le mette in un dizionario
conf=MyOpen.ReadConfig("config/config.cfg","MyDaemon").read()

#Connessione al gataway
gateway=MyOpen.Gateway(conf["gateway"],int(conf["port"]))

class StartServer:
    
    @cherrypy.expose
    def index(self):
        #variabile che conterra tutta la pagina
        S=""
        #nuovo oggetto generatore
        G=MyWeb.MyWebJQMobile()
        
        #genero inizio html con script standard
        S+=G.initHTML()
                
        #lettura file xml configurazione
        file_xml=open("config/configweb.xml").read()
        config_xml=etree.fromstring(file_xml)
        
        #il primo tag nel file config <PAGINA>
        #separa le varie pagine 
        #"txt" contiene un testo identificativo es. Illuminazione
        #"chi" contiene identificativo sezione openwebnet
        # serve per capire che tipo di pagina generare
        #chi=1 illuminazione
        #chi=2 automatismi
        #chi=4 termoregolazione
        #chi=5 antifurto
        #chi="S" pagina speciale con comandi personalizzati"
            
        #salvo in un dizionario elenco pagine
        dict_pagine=dict()
        for selpag in config_xml.iter("PAGINA"):
            dict_pagine[selpag.attrib["chi"]]=selpag.attrib["txt"]
       
        #ciclo per la pagina
        for pagina in config_xml.iter("PAGINA"):
            nomepagina=pagina.attrib["txt"]
            chi=pagina.attrib["chi"]
            S+=G.openPage(nomepagina)
       
            #genero menu per seleziona pagina
            S+=G.selectMenu("select_page",dict_pagine,nomepagina)

            #inserire qui verifica tipo pagina
            if chi=="1":  #illuminazione
                
                #Menu Tabs
                tabs=list()
                for tab in pagina.iter("TAB"):
                    tabs.append(tab.attrib["txt"])
                S+=G.tabsMenu(tabs)

                #Ciclo tab
                for tab in pagina.iter("TAB"):
                    nometab=tab.attrib["txt"]
                    S+=G.openTab(nometab)
                
                    #gruppo collapsable
                    S+=G.openCollapsibleSet()

                    for gruppo in tab.iter("GRUPPO"):
                        nomegruppo=gruppo.attrib["txt"]
                        S+=G.openCollapsible(nomegruppo)
                        
                        for punto in gruppo.iter("PUNTO"):
                            #dove=punto.attrib["dove"]
                            
                            S+=G.openControlGroup()

                            for pulsante in punto.iter("PULSANTE"):
                                #il valore del pulsante deve essere 
                                #un dizionario codificato in stringa
                                #chi - dove - cosa
                                nomepulsante=pulsante.text
                                cod=pulsante.attrib["cod"]
                               
                                #invoco un metodo per generare il codice pulsante
                                codice=urllib.quote(cod)

                                if cod=="null":
                                    stile="style='width:80px'"
                                else:
                                    stile="style='width:30px'"

                                S+=G.button(nomepulsante,codice,stile)    
                            
                            S+=G.closeControlGroup()
                            
                        S+=G.closeCollapsible()


                    S+=G.closeCollapsibleSet()

                    S+=G.closeTab(nometab)
        
            S+=G.closePage(nomepagina)
        
        #invio tutto al server
        yield S
    
    @cherrypy.expose
    def request(self, **data):
        val=data.values()[0]
        #decodifico il dizionario
        cmd=urllib.unquote(val)
        print cmd
        print gateway.sendcmd(cmd)


cherrypy.quickstart(StartServer(), config="lib/web.conf")
