#/usr/bin/python

import os
import signal
import subprocess
import time

#absolute directory
abs_dir=os.path.dirname(os.path.realpath(__file__))

#MyServer.py
#si occupa di avviare i server MyDaemon e MyWebServer
#attualmente senza nessun argomento kill esistenti ed avvia nuovi

#definisco variabili generali
nohup="/usr/bin/nohup"
python="/usr/bin/python"
dirpid=abs_dir+"/log/"
null=open('/dev/null', 'w')

mymonitor=abs_dir+"/lib/MyMonitor.py"
pid_mymonitor=dirpid+'MyMonitor.pid'

mywebserver=abs_dir+"/lib/MyWebServer.py"
pid_mywebserver=dirpid+'MyWebServer.pid'

#fermo
try:
    pid=open(pid_mymonitor,"r").read()
    print "fermo MyMonitor "+pid
    os.kill(int(pid),signal.SIGKILL)
except:
    pass
try:
    pid=open(pid_mywebserver,"r").read()
    print "fermo MyWebServer "+pid
    os.kill(int(pid),signal.SIGKILL)
except:
    pass
time.sleep(2)
#avvio
proc_mymonitor=subprocess.Popen([nohup,python,mymonitor],stdout=null,stderr=null,preexec_fn=os.setpgrp)
print "Avvio myMonitor "+ str(proc_mymonitor.pid)
open(pid_mymonitor,"w").write(str(proc_mymonitor.pid))    

proc_mywebserver=subprocess.Popen([nohup,python,mywebserver],stdout=null,stderr=null,preexec_fn=os.setpgrp)
print "Avvio MyWebServer "+ str(proc_mywebserver.pid)
open(pid_mywebserver,"w").write(str(proc_mywebserver.pid))    





