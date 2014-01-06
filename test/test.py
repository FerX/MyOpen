<<<<<<< HEAD
import MyOpen
=======
#!/usr/bin/python

from MyOpen import MyOpen
>>>>>>> 3dbdda0d6f3da4128d097cac8257b9eb1aa84351
from time import sleep

X=MyOpen.MyOpenGateway("192.168.1.13",20000)
print "accendo la luce"
print X.sendcmd("*1*1*24##")
sleep(1)
print "spengo la luce"
print X.sendcmd("*1*0*24##")
sleep(1)
print "verifico lo stato uno"
print X.sendcmd("*#1*77##")
print "verifico lo stato tanti"
print X.sendcmd("*#1*2##")
print "comando errato"
print X.sendcmd("*1*1*1224##")


print "spengo 24"
print X.sendcmd("*1*0*24##")
print "spengo 77"
print X.sendcmd("*1*0*77##")

