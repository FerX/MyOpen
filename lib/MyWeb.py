#!/usr/bin/python 

class MyWebJQMobile:
    """Classe per generare i vari componenti jquerymobile
        per interfaccia web"""

    import pickle
    import urllib
    import MyOpen
    import os
    abs_dir=os.path.dirname(os.path.realpath(__file__))

    if abs_dir[-4:] == "/lib":
        abs_dir=abs_dir[:-4]

    #leggi impostazioni da config e le mette in un dizionario
    conf=MyOpen.ReadConfig(abs_dir+"/config/config.cfg","MyMonitor").read()

    #connessione al database
    database=MyOpen.Db(abs_dir+"/log/"+conf["nomedb"])

    def initHTML(self):
        #Genero il primo blocco di codice da inviiare al browser

        return '''<!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=0;" />
        <meta name="viewport" content="width=device-width"/>
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <title></title>
        <link rel="stylesheet" href="jquery/jquery.mobile-1.4.0.min.css" />
        <script src="jquery/jquery-1.9.1.min.js"></script>
        <script src="jquery/jquery.mobile-1.4.0.min.js"></script>
        <style>
            /* App custom styles */
        .ui-controlgroup-controls {width:100% !important;}
        </style>
        <script type="text/javascript">
        $(function() {
            //:button select all button and input element
            $("input.noconferma, button.noconferma").click(function( eventObject ) {
                       var com  = $( this );
                       $.post('/request', com , function(data){ 
                       alert(data)}  );
                        });

            $("input.chiediconferma, button.chiediconferma").click(function( eventObject ) {
                       var com  = $( this );
                       var sino = confirm('sei sicuro ?' );
                       if (sino)
                       {
                       $.post('/request', com  );
                       }else{
                       //tolgo evidenzazione
                       $( this ).prop("checked",false);
                       }
                        });
            
            
            //cambio di pagina
            $("select").change(function( eventObject ) {
                    page=$(this).val()
                    $(":mobile-pagecontainer").pagecontainer("change","#"+page);
                    });
                    
    
            });
        </script>
        

        
        
        </head>
        <body>
        '''
    def closeHTML(self):
        return "\n </body> \n </html>" 

    def openPage(self,nomepagina,header=""):
        S='\n'
        S+='\n <!-- Inizio Pagina %s -->' % (nomepagina)
        S+='\n <div data-role="page" id="%s" style="max-width:800px">' % (self.urllib.quote(nomepagina))
        
        if header!="":
            S+='\n <!-- Inizio Header pagina %s -->' % (nomepagina)
            S+='\n <div data-role="header">'
            S+='\n %s' % (header)
            S+='\n </div>  <!-- fine header-->'
        
        S+='\n <!-- Inizio contenuto pagina %s -->' % (nomepagina)
        S+='\n <div role="main" class="ui-content" style="padding:1px;">'
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
            S+='\n         <option value="%s" %s>%s</option>' % (self.urllib.quote(scelte[x]),sel,scelte[x])
        
        S+='\n </select> \n </div> \n  <!-- Fine menu di selezione -->'
        return S

    def openTabsMenu(self,scelte,tab_select=""):
        S='\n'
        S+='\n <!-- Inizio Tabs Menu -->'
        S+='\n <div data-role="tabs">'
        S+='\n <div data-role="navbar">'
        S+='\n <ul>'
        for x in scelte:
            sel=""
            if x==tab_select:
                sel='class="ui-btn-active"'
            
            S+='\n <li><a href="#%s" data-theme="a" data-ajax="false" %s >%s</a></li>' % (self.urllib.quote(x),sel,x)
        S+='\n </ul> \n</div> \n <!-- Fine Tabs menu --> \n'
        
        return S


    def closeTabsMenu(self):
        S='\n </div>'
        S+='<!-- Fine  Tabs menu %s -->' 
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

    def openCollapsible(self,nome,option=""):
        S='\n <!-- Inizio Collapsible -->'
        S+='\n <div data-role="collapsible" %s>' % (option)
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


    def openListView(self):
        S='\n <!-- Inizio ListView -->'
        S+='\n <ul data-role="listview">' 
        return S

    def closeListView(self):
        S='\n </ul> <!-- Chiuso ListView -->'
        return S


    def openList(self):
        S='\n <!-- Inizio List -->'
        S+='\n <li class="ui-field-contain">' 
        return S

    def closeList(self):
        S='\n </li> <!-- Chiuso List -->'
        return S


    def openGrid(self,tipo):
        S='\n <!-- Inizio Grid -->'
        S+='\n <div class="ui-grid-%s">' % (tipo) 
        return S

    def closeGrid(self):
        S='\n </div> <!-- Chiuso grid -->'
        return S


    def openGridBlock(self,tipo,stile=""):
        S='\n <!-- Inizio GridBlock -->'
        S+='\n <div class="ui-block-%s" %s>' % (tipo,stile) 
        return S

    def closeGridBlock(self):
        S='\n </div> <!-- Chiuso gridBlock -->'
        return S

    
    def openRadio(self):
        S='\n <!-- Inizio Radio Button -->'
        S='\n <form>'
        S+='\n <fieldset data-role="controlgroup" data-type="horizontal">' 
        return S

    def closeRadio(self):
        S='\n </fielset> \n </form> <!-- Chiuso Radio Button -->'
        return S

    def radioButton(self,nome,value,style=""):
        S='\n <input type="radio" name="radio-choice" id="%s"  value="%s" %s>' % (nome,value,style)
        S+='\n <label for="%s">%s</label>' % (nome,nome)
        return S
    
    
    def button(self,nome,value,classe="",style=""):
        S='\n <button class="ui-btn ui-btn-inline %s"  id="%s" value="%s" %s>%s</button>' % (classe,nome,value,style,nome)
        return S

    def generaHeader(self,titolo,scelte):
        S="\n <h1>%s</h1>" % (titolo)
        idpop="pop_"+self.urllib.quote(titolo)
        
        S+="""<a href='#"""
        S+=idpop
        S+="""' data-rel="popup" class="ui-btn ui-corner-all ui-shadow ui-btn-inline ui-icon-bars ui-btn-icon-left ui-btn-a" data-transition="pop">Men&ugrave;</a>
        """
        S+="""\n<div data-role="popup" id='"""
        S+=idpop
        S+="""'data-theme="a">
            <ul data-role="listview" datra-inset="true" style="min-width:210px;">"""
        
        for x in scelte.keys():
            S+='\n <li><a href="#%s">%s</a></li>' % (self.urllib.quote(scelte[x]),scelte[x])

        S+="""</ul>
        </div><!-- /collapsible -->
        """


        return S

    def viewLog(self):
        
        database=self.MyOpen.Db(self.abs_dir+"/log/"+self.conf["nomedb"])
        
        row=database.readsql(30,1,True)
        
        S="\n <!-- View Log-->"
        
        for x in row:
            S+='<div class="ui-grid-a"> \n'
            S+='<div class="ui-block-a" style="width:35%; padding-right: 4px">'
            S+='<div class="ui-bar ui-bar-a" style="height:20px">'
            S+=x[1]
            S+='</div></div>\n'
            S+='<div class="ui-block-b" style="width:65%">'
            S+='<div class="ui-bar ui-bar-a" style="height:20px">'
            S+=x[4]
            S+='</div></div>\n'
            S+='</div>\n'
            S+='<div class="ui-grid-solo"> \n'
            S+='<div class="ui-block-a" >'
            S+='<div class="ui-bar ui-bar-c" style="height:20px">'
            S+=x[5]
            S+='</div></div></div>\n'

        return S
