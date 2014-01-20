#!/usr/bin/python 

class MyWebJQMobile:
    """Classe per generare i vari componenti jquerymobile
        per interfaccia web"""

    import pickle
    import urllib

    def initHTML(self):
        #Genero il primo blocco di codice da inviiare al browser

        return '''<!DOCTYPE html>
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
        <script type="text/javascript">
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
        <body>
        '''

    def openPage(self,nomepagina,header=""):
        S='\n'
        S+='\n <!-- Inizio Pagina %s -->' % (nomepagina)
        S+='\n <div data-role="page" id=%s' % (self.urllib.quote(nomepagina))
        
        if header!="":
            S+='\n <!-- Inizio Header pagina %s -->' % (nomepagina)
            S+='\n <div data-role="header">'
            S+='\n %s' % (header)
            S+='\n <\div>  <!-- fine header-->'
        
        S+='\n <!-- Inizio contenuto pagina %s -->' % (nomepagina)
        S+='\n <div role="main" class="ui-content">'

        return S

    def closePage(self,nomepagina,footer=""):
        S='\n'
        S+='\n </div> <!-- Fine contenuto pagina %s -->' % (nomepagina)
        
        if footer!="":
            S+='\n <!-- Inizio footer pagina %s ' % (nomepagina)
            S+='\n <div data-role="footer">'
            S+='\n %s' % (footer)
            S+='\n </div> <!-- Fine footer-->'
        
        S+='\n </div> <!-- Fine pagina %s -->' % (nomepagina)
        
        return S

    def selectMenu(self,nome,scelte,selezionato):
        '''scelte deve essere un dizionario {chi:nomepagina}'''
        S='\n'
        S+="\n<!-- Inizio Menu di  selezione -->"
        S+='\n <div class="ui-field-contain">'
        S+='\n <select name="%s" id="%s">' % (nome,self.urllib.quote(nome))
        for x in scelte.keys():
            sel=""
            if scelte[x]==selezionato: 
                sel='selected="selected"'
            S+='\n         <option value="%s" %s>%s</option>' % (x,sel,scelte[x])
        
        S+='\n </select> \n </div> \n  <!-- Fine menu di selezione -->'

        return S

    def tabsMenu(self,scelte):
        S='\n'
        S+='\n <!-- Inizio Tabs Menu -->'
        S+='\n <div data-role="tabs">'
        S+='\n <div data-role="navbar">'
        S+='\n <ul>'
        for x in scelte:
            S+='\n <li><a href="#%s" data-theme="a" data-ajax="false">%s</a></li>' % (self.urllib.quote(x),x)
        S+='\n </ul> \n</div> \n <!-- Fine Tabs menu --> \n'
        
        return S

    def openTab(self,nome):
        S='\n'
        S+='\n <!-- Inizio Tab %s -->' % (nome)
        S+= '\n <div id="%s" class="ui-content" style="padding:0">' % (self.urllib.quote(nome))
        return S
    
    def closeTab(self,nome):
        S='\n </div>'
        S+='<!-- Fine  Tab %s -->' % (nome)
        return S

    
    def openCollapsibleSet(self):
        S='\n <!-- Inizio Collapsible Set -->'
        S+='\n <div data-role="collapsible-set" data-theme="a" data-content-theme="a">'
        return S

    def closeCollapsibleSet(self):
        S='\n </div> <!-- Chiuso Collapsible Set -->'
        return S

    def openCollapsible(self,nome):
        S='\n <!-- Inizio Collapsible -->'
        S+='\n <div data-role="collapsible">'
        S+='\n <h3> %s </h3>' % (nome)
        return S

    def closeCollapsible(self):
        S='\n </div> <!-- Chiuso Collapsible -->'
        return S

    def openControlGroup(self):
        S='\n <!-- Inizio ControlGroup -->'
        S+='\n <div data-role="controlgroup" data-type="horizontal">' 
        return S

    def closeControlGroup(self):
        S='\n </div> <!-- Chiuso ControlGroup -->'
        return S

    def button(self,nome,value,style=""):
        S='\n <button class="ui-btn ui-btn-inline"  value="%s" %s>%s</button>' % (value,style,nome)
        return S


