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
            header_pagina=G.generaHeader(nomepagina,dict_pagine)

            S+=G.openPage(nomepagina,header_pagina)
             
            
            #inserire qui verifica tipo pagina
            if True: #per ora resta tutto uguale 
                
                #Menu Tabs
                tabs=list()
                for tab in pagina.iter("TAB"):
                    tabs.append(tab.attrib["txt"])
                S+=G.openTabsMenu(tabs)

                #Ciclo tab
                for tab in pagina.iter("TAB"):
                    nometab=tab.attrib["txt"]
                    S+=G.openTab(nometab)
                
                    #gruppo collapsable
                    S+=G.openCollapsibleSet()

                    for gruppo in tab.iter("GRUPPO"):
                        nomegruppo=gruppo.attrib["txt"]
                        S+=G.openCollapsible(nomegruppo)
                        
                        S+=G.openListView()

                        for punto in gruppo.iter("PUNTO"):
                            nomepunto=punto.attrib["txt"]
                            
                            #predisposizione commento 
                            notapunto=""
                            
                            S+=G.openList()
                           
                            S+=G.openGrid("a")
                            
                            S+=G.openGridBlock("a","style='width:50%'")
                            S+="<h3>%s</h3><p>%s</p>" % (nomepunto,notapunto)
                            S+=G.closeGridBlock()

                            S+=G.openGridBlock("b","style='width:50%'")
                            
                            
                            S+=G.openRadio()

                            for pulsante in punto.iter("PULSANTE"):
                                #il valore del pulsante deve essere 
                                #un dizionario codificato in stringa
                                #chi - dove - cosa
                                nomepulsante=pulsante.text
                                cod=pulsante.attrib["cod"]
                               
                                codice=urllib.quote(cod)
                                stile=""
                                S+=G.radioButton(nomepulsante,codice,stile)    
                                    
                            S+=G.closeRadio()
                            S+=G.closeGridBlock()

                            S+=G.closeGrid() 
                            S+=G.closeList()
                        
                        S+=G.closeListView()
                        
                        S+=G.closeCollapsible()


                    S+=G.closeCollapsibleSet()

                    S+=G.closeTab(nometab)
        
                S+=G.closeTabsMenu()
            
            S+=G.closePage(nomepagina)
        
        S+=G.closeHTML()

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
