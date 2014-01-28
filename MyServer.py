#/usr/bin/python
import os
import signal
import subprocess
import time

#MyServer.py
#si occupa di avviare i server MyDaemon e MyWebServer

#definisco variabili generali
nohup="/usr/bin/nohup"
python="/usr/bin/python"
dirpid="log/"
null=open('/dev/null', 'w')

mymonitor="lib/MyMonitor.py"
pid_mymonitor=dirpid+'MyMonitor.pid'

mywebserver="lib/MyWebServer.py"
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





