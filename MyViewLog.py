#!/usr/bin/python

#MyViewLog.py
#consente di visualizzare e scorrere i log dell'impianto

#utilizzo la libreria urwid
#per poter visualizzare i contenuti, fare il parsing del codice, 
#sfogliare le pagine ... ed in futuro implementare ricerche o altro

import curses
from lib import MyOpen
import time
import sys
import os
abs_dir=os.path.dirname(os.path.realpath(__file__))

if abs_dir[-4:] == "/lib":
    abs_dir=abs_dir[:-4]

#leggi impostazioni da config e le mette in un dizionario
conf=MyOpen.ReadConfig(abs_dir+"/config/config.cfg","MyMonitor").read()

#connessione al database
database=MyOpen.Db(abs_dir+"/log/"+conf["nomedb"])


#inizializzo gestore schermo
S=curses.initscr()
curses.start_color()
#attivo noecho tastiera
curses.noecho()
curses.cbreak()
S.keypad(1)
#recupero numero righe e col disponibili
R,C=S.getmaxyx()
R=R-2
C=C-2
fine=False
sino_parsing=False

#pair dei colori
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

def scrivi(pagina,sino_parsing):
    row=database.readsql(R,pagina,sino_parsing)
    riga=1
    for x in row:
        S.addstr(riga,1,x[1])
        S.addstr(riga,len(x[1])+2,x[4],curses.color_pair(3))
        tronca=C-(20+len(x[4]))
        S.addstr(riga,20+len(x[4]),x[5][:tronca])
        riga+=1
    
    S.refresh()
    #ritorno quante righe ho scritto
    return len(row)

def aiuto():
    H=curses.newwin(11,40,10,20)
    H.border()
    H.addstr(0,10,"[HELP]",curses.color_pair(2))
    H.addstr(2,2,"Su/PagSu = Scorri in su",curses.color_pair(2))
    H.addstr(4,2,"Giu/PagGiu = Scorri in giu",curses.color_pair(2))
    H.addstr(6,2,"p = Attiva/disattiva parsing",curses.color_pair(2))
    H.addstr(8,2,"Esc / q = Esci dal programma",curses.color_pair(2))

    c = H.getch()


pagina=0
while True:
    S.erase()
    S.border()
    numrighescritte=scrivi(pagina,sino_parsing)
    #num pagina
    S.addstr(R+1,C-20,"["+str(pagina)+":"+str(pagina+R)+"]",curses.color_pair(2))   
    #comandi
    #testata
    #S.addstr(R+1,5,"[Esc/q=esci]" parsing]",curses.color_pair(2))   
    S.addstr(R+1,5,"[F1=HELP]",curses.color_pair(2))   
    
    S.addstr(0,5,"[ VISUALIZZAZIONE DI LOG - MyOpenWebNet]",curses.color_pair(2))   

    while True: 
        c = S.getch()
        
        S.addstr(0,0,str(c))
        #se premo ESC o q
        if c == 113 or c == 27:  
            curses.endwin()
            sys.exit()
        #pagina su o tasto su
        elif c == 259 or c == 339:
            pagina-=R
            if pagina<0: pagina=0
            break
        #pagina giu 
        elif c == 258 or c == 338:
            if not numrighescritte<R:
                pagina+=R
            break
        #attiva/disattiva parsing 
        elif c == 112:
            if sino_parsing:
                sino_parsing=False
            else:
                sino_parsing=True
            break
        #h o f1 - help
        
        elif c == 104 or c == 265:
            aiuto()
            break


