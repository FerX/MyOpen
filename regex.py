#!/usr/bin/python
#definizione liste per regex
#per maggior lettura del codice considero che gli * verranno convertiti in X e che gli ultimi ## verranno tolti
#es. tempCOD=self.COD.replace("*","X").rstrip("##")
#
# Varabili speciali
# A1,A2,An --> WHAT
# B1,B2,Bn --> WHERE
# 

#lista WHO=0
W0=[]
#Attivazione Scenario *0*scenario*dove
W0.append([r"^X0X(?P<WHAT>\d\d)X(?P<WHERE>\d\d)(?P<INT>#\d#\d)?$","Attivazione scenario WHAT nella centralina WHERE INT"])
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

