#!/usr/bin/python 

import cherrypy

#importo il mio file dove definisco le var statiche
from lxml import etree
import pickle
import urllib
import MyOpen

#leggi impostazioni da config e le mette in un dizionario
conf=MyOpen.ReadConfig("../config/config.cfg","MyDaemon").read()

#Connessione al gataway
gateway=MyOpen.Gateway(conf["gateway"],int(conf["port"]))



class StartServer:
    """ Sample request handler class. """
    @cherrypy.expose
    def index(self):

        yield '''<!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=0;" />
        <meta name="viewport" content="width=device-width"/>
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <title>
        </title>
        <link rel="stylesheet" href="jquery/jquery.mobile-1.4.0.min.css" />
        <style>
            /* App custom styles */
        </style>
        <script src="jquery/jquery-1.9.1.min.js">
        </script>
        <script src="jquery/jquery.mobile-1.4.0.min.js">
        </script>
        '''
        #codice javascript che riceve la pressione del pulsante 
        yield '''<script type="text/javascript">
        $(function() {
            //stop the page from doing a stretch from the top when dragged ;
            //document.ontouchmove = function(event){ event.preventDefault(); };
            //move beyond the address  bar to hide ;
            //window.scrollTo(0, 1);
            $("button").click(function( eventObject ) {
                       var com  = $( this );
                       $.post('/request', com  );
                       return false;
                        });
            });
        </script>
        </head>
        '''
        #lettura file xml configurazione
        file_xml=open("../config/configweb.xml").read()
        config_xml=etree.fromstring(file_xml)
        
        yield "\n <body>"
        
        #inizializzazione tabs
        menu_tabs='\n <div data-role="tabs">'
        menu_tabs+='\n <div data-role="navbar">'
        menu_tabs+='\n <ul>'
        for pagina in config_xml.iter("Pagina"):
            menu_tabs+='\n <li><a href="#%s" data-theme="a" data-ajax="false">%s</a></li>' % \
                    (pagina.attrib["txt"],pagina.attrib["txt"])
        
        menu_tabs+='\n </ul> \n</div>'
        yield menu_tabs
        
        #### Pagina
        for pagina in config_xml.iter("Pagina"):
            
            nomepagina=pagina.attrib["txt"] 
            chi=pagina.attrib["chi"]
            
            #Inizializzazione nuovo tabs
            yield '\n <div id="%s" class="ui-content" style="padding:0">' % (nomepagina)
            
            #Header Pagina
            yield "\n <div data-role='header'>"
            #yield "\n <h1> %s </h1>" % (nomepagina)
            yield "\n </div>" 
            
            #contenuto pagina
            yield '\n <div role="main" class="ui-content" style="padding:1px">'

            #definizione collapsible set
            yield '\n <div data-role="collapsible-set" data-theme="a" data-content-theme="a">'
            
            for sezione in pagina.iter("Sezione"):
                
                nomesezione=sezione.attrib["txt"]

                #collapsible
                yield '\n <div data-role="collapsible">'
                yield '\n      <h3> %s </h3>' % (nomesezione)


                for punto in sezione.iter("Punto"):
                    
                    nomepunto=punto.attrib["txt"]
                    dove=punto.attrib["dove"]
                    

                    #bottone
                    #ogni bottone contiene in value tutte le informazioni serializzate
                    #un dizionario con i seguenti campi
                    #chi:1,dove:77,cosa:on/off,comando

                    #definizione gruppo di pulsanti
                    yield '\n <div data-role="controlgroup" data-type="horizontal">' 
                    
                    val={"chi":chi,"dove":dove,"cosa":"setting"}
                    #rendo il dizionario una stringa codificata
                    cod_val=urllib.quote(pickle.dumps(val))
                   
                    #pulsante principale - premendolo apre le impostazioni
                    yield '\n <button class="ui-btn ui-btn-inline"  value="%s" \
                            style="width:90px"> %s</button>' % (cod_val,nomepunto)
                    
                    #genera i pulsanti per i vari comandi
                    for setting in punto.iter("Comando"):
                        cosa=setting.text                    
                        val={"chi":chi,"dove":dove,"cosa":cosa}
                        #rendo il dizionario una stringa codificata
                        cod_val=urllib.quote(pickle.dumps(val))
                        yield '\n <button class="ui-btn ui-btn-inline" value="%s">%s</button>' % (cod_val,cosa)
                    
                    yield '\n </div>'

                #chiusura collapsible
                yield '\n </div>'
            
            #Chiusura collapsible set
            yield "\n </div>"
            #Chiusura contenuto pagina
            yield "\n </div>"

            #Footer pagina
            yield "\n <div data-role='footer'>"
            yield "\n </div>"

            #Chiusura pagina
            yield "\n </div>"

        #menu pagine
        yield menu_tabs
        
        yield '''
        \n </body>
        \n </html>
        '''
    @cherrypy.expose
    def request(self, **data):
        val=data.values()[0]
        #decodifico il dizionario
        val=pickle.loads(urllib.unquote(val))
        print "data form: "+str(val)
        chi=val["chi"]
        dove=val["dove"]
        cosa=val["cosa"]
        if cosa=="ON":
            cosa_cmd="1"
        elif cosa=="OFF":
            cosa_cmd="0"
        else:
            cosa_cmd=""

        cmd="*"+chi+"*"+cosa_cmd+"*"+dove+"##"

        print cmd
        print gateway.sendcmd(cmd)


cherrypy.quickstart(StartServer(), config="web.conf")
