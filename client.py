#!/usr/bin/env python3
import socket
import select
import threading
import sys

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
try:
    s.connect((sys.argv[1],7777))
except Exception as e:
    #print(e)
    input("Erreur de connexion au serveur ! Appuyer sur n'importe quelle touche pour sortir")
    sys.exit()

while True:
    data = s.recv(1500)
    print(data)
s.close()
