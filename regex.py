#!/usr/bin/python
#definizione liste per regex
#per maggior lettura del codice considero che gli * verranno convertiti in X e che gli ultimi ## verranno tolti
#es. tempCOD=self.COD.replace("*","X").rstrip("##")
#
# Varabili usate nelle regex per definire la sostituzione
# la prima lettera definisce a cosa si riferisce
# A=WHAT(cosa) - B=WHERE(dove) - etc. etc-
# la seconda lettera un numero progressivo 1...n
# A1 ... A2 .. B1 .. B2
# ultima lettera identifica se va tradotto
# se ultima lettera = H (human) va interpretato il valore in base alla prima lettera

#Standard Variable
e="$" #end of regex
x="X" # X simbol - substitute of *

#lista WHO=0 - gestione scenari
W0=[]

s="^X0"  #start of regex
cosa="(?P<A1H>([1-9]|[12][0-9]|3[0-2]))"
dove="(?P<B1H>\d\d(#\d#\w)?)"
#Attivazione Scenario *0*cosa(1-32)*dove
W0.append([r""+s+x+cosa+x+dove+e,"Attivazione scenario {A1H} nella centralina {B1H}"])
#Disattivazione Scenario *0*cosa#0*dove
W0.append([r""+s+x+cosa+"#0"+x+dove+e,"Disattivazione scenario {A1H} nella centralina {B1H}"])
#Inizio programmazione Scenario *0*40#scenario*dove
W0.append([r""+s+x+"40#"+cosa+x+dove+e,"Inizio programmazione scenario {A1H} nella centralina {B1H}"])
#Fine programmazione Scenario *0*41#scenario*dove
W0.append([r""+s+x+"41#"+cosa+x+dove+e,"Fine programmazione scenario {A1H} nella centralina {B1H}"])
#Cancella tutti gli scenari *0*42*dove
W0.append([r""+s+"42"+x+dove+e,"Cancellazione di tutti gli scenari nella centralina {B1H}"])
#Cancella scenario *0*42#scenario*dove
W0.append([r""+s+x+"42#"+cosa+x+dove+e,"Cancellazine scenario {A1H} nella centralina {B1H}"])
#Blocca centralina scenari *0*43*dove
W0.append([r""+s+x+"43"+x+dove+e,"Blocco centralina scenari {B1H}"])
#Sblocca centralina scenari *0*44*dove
W0.append([r""+s+x+"44"+x+dove+e,"Sblocco centralina scenari {B1H}"])
#Centralina comandi non disponibile *0*45*dove
W0.append([r""+s+x+"45"+x+dove+e,"Centralina comandi {B1H} non disponibile"])
#Memoria Centralina scenari piena *0*46*dove
W0.append([r""+s+x+"46"+x+dove+e,"Centralina comandi {B1H} piena"])

#lista WHO=1 - gestione illuminazione
W1=[]

s="^X1"  #start of regex
cosa="(?P<A1H>([0-9]|[12][0-9]|3[0-1]))"
dove="(?P<B1H>\w?\d(#\d#\w)?)"
livello="(?P<L1>\d{1,3})"
velocita="(?P<V1>\d{1,3})"
time="(?P<O1>\d{1,3})X(?P<M1>\d{1,2})X(?P<S1>\d{1,2})"
#Accensione-spegnimento *1*cosa*dove
W1.append([r""+s+x+cosa+x+dove+e,"{A1H} in {B1H}"])
#Variazione intensita *#1*dove*1*livello*velocita
W1.append([r""+x+"#1"+x+dove+x+"1"+x+livello+x+velocita+e,"Variazione intensita {B1H} in {L1} alla velocita {V1}"])
#Temporizzazione *#1*dove*2*ore*minuti*secondi
W1.append([r""+x+"#1"+x+dove+x+"2"+x+time+e,"Temporizzazione {B1H} ore {O1} minuti {M1} secondi {S1}"])


#lista WHO=2 - automatismi
W2=[]

s="^X2"  #start of regex
cosa="(?P<A1H>[012])"
dove="(?P<B1H>\S?\d(#\d#\w)?)"
#Automazione *2*cosa*dove
W2.append([r""+s+x+cosa+x+dove+e,"{A1H} in {B1H}"])


W3=[]
W4=[]
W5=[]
W7=[]
W9=[]
W13=[]
W15=[]
W16=[]
W17=[]
W1001=[]
W1004=[]
W1013=[]



