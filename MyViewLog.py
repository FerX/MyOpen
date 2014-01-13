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

#leggi impostazioni da config e le mette in un dizionario
conf=MyOpen.ReadConfig("config/config.cfg","MyDaemon").read()

#connessione al database
database=MyOpen.Db("log/"+conf["nomedb"])

#connessione al parser
parser=MyOpen.Parser()

#inizializzo gestore schermo
S=curses.initscr()

#attivo noecho tastiera
curses.noecho()
curses.cbreak()
S.keypad(1)
#recupero numero righe e col disponibili
R,C=S.getmaxyx()
R=R-2
C=C-2
fine=False

def readsql(limit,offset):
    sql="SELECT ID,TIME,WHO,WHE,COD FROM LOG ORDER BY ID DESC LIMIT "+str(limit)+" OFFSET "+str(offset)
    database.cursor.execute(sql)
    Sret=[]
    conta=0
    for r in database.cursor.fetchall():
        id=r[0]
        t=time.localtime(float(r[1]))
        stime=str(t[3]).rjust(2,"0")+":"+str(t[4]).rjust(2,"0")+":"+str(t[5]).rjust(2,"0")+" "+str(t[2]).rjust(2,"0")+"-"+str(t[1]).rjust(2,"0")+"-"+str(t[0]).rjust(2,"0")
        who=r[2]
        whe=r[3]
        cod=r[4]
        pars=parser.parsing(cod)
        Sret.append([str(id),stime,str(who),str(whe),cod,str(pars)])
        conta+=1
    global fine
    fine=False
    if conta<limit:
        fine=True
    return Sret

        

def scrivi(pagina):
    row=readsql(R,pagina)
    riga=1
    for x in row:
        output=x[1]+" "+x[4]+" "+x[5]
        S.addstr(riga,1,output)
        riga+=1
    S.refresh()

pagina=0
while True:
    S.erase()
    S.border()
    scrivi(pagina)
    #num pagina
    S.addstr(R+1,C-20,"["+str(pagina)+":"+str(pagina+R)+"]")   
    #comandi
    S.addstr(R+1,5,"[ SU-PAGSU GIU-PAGGIU  ESC o q]")   
    #testata
    S.addstr(0,5,"[ VISUALIZZAZIONE DI LOG - MyOpenWebNet]")   

    while True: 
        c = S.getch()
        #se premo ESC o q
        if c == 113 or c == 27:  
            curses.endwin()
            sys.exit(c)
        #pagina su o tasto su
        elif c == 259 or c == 339:
            pagina-=R
            if pagina<0: pagina=0
            break
        #pagina giu 
        elif c == 258 or c == 338:
            if not fine:
                pagina+=R
            break
