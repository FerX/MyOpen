#!/usr/bin/python 

import cherrypy

#importo il mio file dove definisco le var statiche
import static
from lxml import etree

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
            
            $("#send").submit(function() {
                       var com = {nome:$("#comando").val()}; 
                       $.post('/request', com);
                       return false;
                        });
            });
        </script>
        </head>
        '''

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
        
        for pagina in root.iter("Pagina"):
            #yield "<br>pagina.tag %s" % (pagina.tag)
            #yield "<br>pagina.text %s" % (pagina.text)
            #yield "<br>pagina.attrib %s" % (pagina.attrib)
            
            nomepagina=pagina.attrib["txt"] 
            
            #Inizializzazione nuovo tabs
            yield '\n <div id="%s" class="ui-content">' % (nomepagina)
            
            #Header Pagina
            yield "\n <div data-role='header'>"
            #yield "\n <h1> %s </h1>" % (nomepagina)
            yield "\n </div>" 
            
            #contenuto pagina
            yield "\n <div role='main' class='ui-content'>"

            #definizione collapsible set
            yield '\n <div data-role="collapsible-set" data-theme="a" data-content-theme="a">'
            
            for sezione in pagina.iter("Sezione"):
                #yield "<br>---sezioni.tag %s" % (sezioni.tag)
                #yield "<br>---sezioni.text %s" % (sezioni.text)
                #yield "<br>---sezioni.attrib %s" % (sezioni.attrib)
                
                nomesezione=sezione.attrib["txt"]

                #collapsible
                yield '\n <div data-role="collapsible">'
                yield '\n      <h3> %s </h3>' % (nomesezione)


                for punto in sezione.iter("Punto"):
                    #yield "<br>------punti.tag %s" % (punti.tag)
                    #yield "<br>------punti.text %s" % (punti.text)
                    #yield "<br>------punti.attrib %s" % (punti.attrib)
                    nomepunto=punto.attrib["txt"]

                    #bottone
                    yield '\n <div data-role="controlgroup" data-type="horizontal">' 
                    yield '\n <a href="#" class="ui-btn">%s</a>' % (nomepunto)
                    yield '\n <a href="?a=0101" class="ui-btn">%s</a>' % ("ON")
                    yield '\n <a href="/request" class="ui-btn">%s</a>' % ("OFF")
                    yield '\n <form id="send" action"#" method="post">'
                    yield '\n <input type="hidden" id="comando" value="*1*1*77">'
                    yield '\n <input type="submit" value="ON">'
                    yield '\n </form>'
                    yield '\n </div>'
                    for setting in punto.iter("*"):
                        #yield "\n <br>---------setting.tag  %s" % (setting.tag)
                        #yield "\n <br>---------setting.text %s" % (setting.text)
                        #yield "\n <br>---------setting.attrib %s" % (setting.attrib)
                        pass 

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
        print "nome: "+str(data)
        #key = data['key_pressed'].lower()
        #print "fatto: "+str(data)
            
cherrypy.quickstart(StartServer(), config="web.conf")
