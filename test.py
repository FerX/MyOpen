from MyOpen import MyOpen

S=MyOpen("192.168.1.7",20000)
S.connect(monitor=0)
print "accendo la luce"
S.send("*1*1*77##")
print "verifico lo stato"
S.send("*#1*77##")
for x in range(10):
    print x
    print S.read()

print "spengo la luce"
S.send("*1*0*77##")
print "verifico lo stato"
S.send("*#1*77##")
for x in range(10):
    print S.read()

