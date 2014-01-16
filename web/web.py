#!/usr/bin/python 

import cherrypy

#importo il mio file dove definisco le var statiche
import static
from lxml import etree
import pickle

class StartServer:
    """ Sample request handler class. """
    @cherrypy.expose
    def index(self):
        yield static.HEADER
        
        #lettura comandi
        
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
        file_xml=open("config.xml").read()
        root=etree.fromstring(file_xml)
        
        yield "\n <body>"
        
        #inizializzazione tabs
        menu_tabs='\n <div data-role="tabs">'
        menu_tabs+='\n <div data-role="navbar">'
        menu_tabs+='\n <ul>'
        for pagina in root.iter("Pagina"):
            menu_tabs+='\n <li><a href="#%s" data-theme="a" data-ajax="false">%s</a></li>' % \
                    (pagina.attrib["txt"],pagina.attrib["txt"])
        
        menu_tabs+='\n </ul> \n</div>'
        yield menu_tabs
        
        #pagina
        for pagina in root.iter("Pagina"):
            
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
                    #yield "<br>------punti.tag %s" % (punti.tag)
                    #yield "<br>------punti.text %s" % (punti.text)
                    #yield "<br>------punti.attrib %s" % (punti.attrib)
                    
                    nomepunto=punto.attrib["txt"]
                    dove=punto.attrib["dove"]
                    

                    #bottone
                    #ogni bottone contiene in value tutte le informazioni serializzate
                    #un dizionario con i seguenti campi
                    #chi:1,dove:77,cosa:on/off,comando

                    #definizione gruppo di pulsanti
                    yield '\n <div data-role="controlgroup" data-type="horizontal">' 
                    
                    val={"chi":chi,"dove":dove,"cosa":"setting"}
                    cod_val=pickle.dumps(val,2)
                    #pulsante principale
                    yield '\n <button class="ui-btn ui-btn-inline"  value="%s" style="width:90px"> %s</button>' % (cod_val,nomepunto)
                    for setting in punto.iter("*"):
                        #yield "\n <br>---------setting.tag  %s" % (setting.tag)
                        #yield "\n <br>---------setting.text %s" % (setting.text)
                        #yield "\n <br>---------setting.attrib %s" % (setting.attrib)
                        pass
                    
                    yield '\n <button class="ui-btn ui-btn-inline"  value="provaon">ON</button>'
                    yield '\n <button class="ui-btn ui-btn-inline"  value="provaoff">OFF</button>'
                    
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
        # Then to access the data do the following
        print "data: "+str(data)
        #for x in data.keys():
        #    print str(data[x])
        val=data.values()[0]
        val=pickle.loads(val)
        print "data form: "+str(val)
            
cherrypy.quickstart(StartServer(), config="web.conf")
