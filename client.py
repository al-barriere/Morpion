#!/usr/bin/env python3
import socket
import select
import threading
import sys
#from grid import *

whoIAm = "spectator"
#grids = [grid(), grid()] #une logique et une graphique, différentes si joueur, identique si spectateur
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
try:
    s.connect((sys.argv[1],7777))
except Exception as e:
    input("Erreur de connexion au serveur ! Appuyer sur n'importe quelle touche pour sortir")
    sys.exit()

while True:
    data = s.recv(1500)
    input("coucou")
    if data.decode("utf-8") == "J1" :
        whoIAm = "J1"
        break
    else if data.decode("utf-8") == "J2" :
        whoIAm = "J2"
        break

print(whoIAm)
input("BLBLB")
#while grids[0].gameOver() == -1 :
#    pass
s.close()
