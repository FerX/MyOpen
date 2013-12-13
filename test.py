from MyOpen import MyOpen
from time import sleep

S=MyOpen("192.168.1.7",20000)
S.connect()
#print "accendo la luce"
#print S.send("*1*1*1177##")
#sleep(1)
#print "spengo la luce"
#print S.send("*1*0*77##")
#sleep(1)
print "verifico lo stato"
print S.send("*#1*7##")
s.close()
