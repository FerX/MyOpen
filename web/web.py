#!/usr/bin/python

import cherrypy

#importo il mio file dove definisco le var statiche
import static

class StartServer:
    """ Sample request handler class. """
    @cherrypy.expose
    def index(self):
        yield static.HEADER
        yield '''<script type="text/javascript">
        $(document).ready(function() {
            //stop the page from doing a stretch from the top when dragged ;
            document.ontouchmove = function(event){ event.preventDefault(); };
            //move beyond the address  bar to hide ;
            window.scrollTo(0, 1);
            //start button click code;
            $("#prova").click(function () {$.post('/request',{key_pressed:"prova"})});
            $("#start").click(function () {$.post('/request',{key_pressed:"start"})});
            $("#enter").click(function () {$.post('/request',{key_pressed:"enter"})});
            $("#esc").click(function () {$.post('/request',{key_pressed:"esc"})});
            $("#power").change(function () {$.post('/request',{key_pressed:"power_"+$(this).val()})});
        });
        </script>
        </head>
        <body style="overflow: hidden;overflow-x:hidden;">
            <div data-role="page" data-theme="a" id="page1">
                <div data-theme="a" data-role="header" data-position="">
                    <h5>
                    MyOpenWebNet - Controllo Remoto - FerX
                    </h5>
                </div>
            <div data-role="content">
                <div class="ui-grid-b">
                    <div class="ui-block-a">
                        <button type="button" id="prova" data-role="button" data-transition="fade" >
                            Prova
                        </button>
                    </div>
                    <div class="ui-block-b">
                        <button type="button" id="start" data-role="button" data-transition="fade" >
                            Start
                        </button>
                    </div>
                    <div class="ui-block-a">
                        <button type="button" id="enter" data-role="button" data-transition="fade">
                            Enter
                        </button>
                    </div>
                    <div class="ui-block-b">
                        <button type="button" id="esc" data-role="button" data-transition="fade">
                            Esc
                        </button>
                    </div>

                </div>
                <div data-role="fieldcontain">
                    <fieldset data-role="controlgroup">
                        <label for="power">
                        </label>
                        <select name="power" id="power" data-theme="a" data-role="slider">
                            <option value="off">
                                Off
                            </option>
                            <option value="on">
                                On
                            </option>
                        </select>
                    </fieldset>
                </div>
            </div>
        </div>
        <script>
            //App custom javascript
        </script>
        </body>
        </html>
        '''
    @cherrypy.expose
    def request(self, **data):
        # Then to access the data do the following
        #print data
        key = data['key_pressed'].lower()
        print key
            
cherrypy.quickstart(StartServer(), config="web.conf")
