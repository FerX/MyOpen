#!/usr/bin/python
#definizione liste per regex
#per maggior lettura del codice considero che gli * verranno convertiti in X e che gli ultimi ## verranno tolti
#es. tempCOD=self.COD.replace("*","X").rstrip("##")
#
# Varabili usate nelle regex per definire la sostituzione
# la prima lettera definisce a cosa si riferisce
# A=WHAT - B=WHERE - etc. etc-
# la seconda lettera un numero progressivo 1...n
# A1 ... A2 .. B1 .. B2
# ultima lettera identifica se va tradotto
# se ultima lettera = H (human) va interpretato il valore in base alla prima lettera

#lista WHO=0 - gestione scenari
W0=[]
#Attivazione Scenario *0*scenario*dove
W0.append([r"^X0X(?P<A1H>\d\d)X(?P<B1H>\d\d(#\d#\d)?)$",\
        "Attivazione scenario {A1H} nella centralina {B1H}"])
#Disattivazione Scenario *0*scenario#0*dove
W0.append(r"^X0X(?P<WHAT>\d\d)#0X(?P<WHERE>\d\d)(?P<INT>#\d#\d)?$")
#Inizio programmazione Scenario *0*40#scenario*dove
W0.append(r"^X0X40#(?P<WHAT>\d\d)X(?P<WHERE>\d\d)(?P<INT>#\d#\d)?$")
#Fine programmazione Scenario *0*41#scenario*dove
W0.append(r"^X0X41#(?P<WHAT>\d\d)X(?P<WHERE>\d\d)(?P<INT>#\d#\d)?$")
#Cancella tutti gli scenari *0*42*dove
W0.append(r"^X0X42X(?P<WHERE>\d\d)(?P<INT>#\d#\d)?$")
#Cancella scenario *0*42#scenario*dove
W0.append(r"^X0X42#(?P<WHAT>\d\d)X(?P<WHERE>\d\d)(?P<INT>#\d#\d)?$")
#Blocca centralina scenari *0*43*dove
W0.append(r"^X0X43X(?P<WHERE>\d\d)(?P<INT>#\d#\d)?$")
#Sblocca centralina scenari *0*43*dove
W0.append(r"^X0X44X(?P<WHERE>\d\d)(?P<INT>#\d#\d)?$")
#Centralina comandi non disponibile *0*45*dove
W0.append(r"^X0X45X(?P<WHERE>\d\d)(?P<INT>#\d#\d)?$")
#Memoria Centralina scenari piena *0*46*dove
W0.append(r"^X0X45X(?P<WHERE>\d\d)(?P<INT>#\d#\d)?$")

#lista WHO=1 - gestione illuminazione
W1=[]
#Accensione *1*cosa*dove
W0.append(r"^X1X(?P<WHAT>\d\d)X(?P<WHERE>\d\d)(?P<INT>#\d#\d)?$")
#Variazione intensita *#1*dove*1*livello*velocita
W0.append(r"^X1X(?P<WHERE>\d\d)(?P<INT>#\d#\d)?X1X(?P<LIVELLO>\d{1,3})(?P<VELOCITA>\d{1,3})$")
#Temporizzazione *#1*dove*2*ore*minuti*secondi
W0.append(r"^X#1X(?P<WHERE>\d\d)(?P<INT>#\d#\d)?X2X(?P<ORE>\d{1,3})X(?P<MINUTI>\d{1,2})X(?P<SECONDI>\d{1,2})$")

