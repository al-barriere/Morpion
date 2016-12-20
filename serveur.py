#!/usr/bin/env python3
import socket
import select
import threading
from grid import *
from main import *
import os

nbPlayer = 0
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM,0)
l = []
clientAddr = []

#Effectue les connexions
def f():
    while True:
        lSocket = select.select(l,[],[])[0]
        for newS in lSocket:
            global s
            if s == newS :
                global nbPlayer
                nbPlayer += 1
                otherS, addr = newS.accept()
                global l
                global clientAddr
                clientAddr.append(addr)
                l.append(otherS)

#MAIN
i=0
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
s.bind(('localhost',7777))
s.listen(1)
l.append(s)
os.system('clear')
print("En attente de joueurs...")
threading.Thread(None,f,None).start()
while True :
    if nbPlayer >= 2 :
        print(nbPlayer,"joueurs sont connectés")
