#!/usr/bin/python 

import cherrypy

#importo il mio file dove definisco le var statiche
from lxml import etree
import urllib
import MyOpen
import MyWeb
import os

abs_dir=os.path.dirname(os.path.realpath(__file__))

if abs_dir[-4:] == "/lib":
    abs_dir=abs_dir[:-4]

#leggi impostazioni da config e le mette in un dizionario
conf=MyOpen.ReadConfig(abs_dir+"/config/config.cfg","MyMonitor").read()

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
        file_xml=open(abs_dir+"/config/configweb.xml").read()
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
                
                #evidenzio il primo
                tab_select=tabs[0]
                S+=G.openTabsMenu(tabs,tab_select)

                #Ciclo tab
                for tab in pagina.iter("TAB"):
                    nometab=tab.attrib["txt"]
                    S+=G.openTab(nometab)
                
                    #gruppo collapsable
                    S+=G.openCollapsibleSet()
                
                    for gruppo in tab.iter("GRUPPO"):
                        nomegruppo=gruppo.attrib["txt"]
                        
                        opzione=""
                        if "aperto" in  gruppo.keys():        
                            aperto=gruppo.attrib["aperto"]
                            if aperto.upper()=="TRUE":
                                opzione='data-collapsed="false"'


                        S+=G.openCollapsible(nomegruppo,opzione)
                        
                        S+=G.openListView()

                        for punto in gruppo.iter("PUNTO"):
                            nomepunto=punto.attrib["txt"]
                            
                            notapunto=""
                            if "nota" in  punto.keys():        
                                notapunto=punto.attrib["nota"]
                            
                            S+=G.openList()
                           
                            S+=G.openGrid("a")
                            
                            S+=G.openGridBlock("a","style='width:40%'")
                            S+="<h3>%s</h3><p>%s</p>" % (nomepunto,notapunto)
                            S+=G.closeGridBlock()

                            S+=G.openGridBlock("b","style='width:60%'")
                            
                            #S+=G.openRadio()

                            for pulsante in punto.iter("PULSANTE"):
                                nomepulsante=pulsante.text
                                cod=pulsante.attrib["cod"]
                        
                            
                                stile='class="noconferma"'
                                classe='noconferma'
                                if "chiediconferma" in pulsante.keys():
                                    chiediconferma=pulsante.attrib["chiediconferma"]
                                    if chiediconferma.upper()=="TRUE":
                                        stile='class="chiediconferma"'
                                        classe='chiediconferma'
                                
                                codice=urllib.quote(cod)
                                #S+=G.radioButton(nomepulsante,codice,stile)    
                                S+=G.button(nomepulsante,codice,classe=classe)    
                                    
                            #S+=G.closeRadio()
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
        return S
    
    @cherrypy.expose
    def request(self, **data):
        val=data.values()[0]
        #decodifico il dizionario
        cmd=urllib.unquote(val)
        print cmd
        ret=gateway.sendcmd(cmd)
        print ret
        yield str(ret)


conf_cherry={ 'global':
        {   'server.socket_host': "0.0.0.0",
            'server.socket_port' :7777,
            'server.thread_pool' :10
            },
        '/':
        { 'tools.staticdir.root' : abs_dir+"/lib"},
        '/jquery':
        {   'tools.staticdir.on' : True,
            'tools.staticdir.dir' : 'jquery'
            }
        }


cherrypy.quickstart(StartServer(), config=conf_cherry)


