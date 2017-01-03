#!/usr/bin/env python3
import socket
import select
import threading
from grid import *
import sys

whoIAm = "spectator"
grid = grid() #une grille graphique uniquement, la logique étant gérée sur le serveur
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

try:
    s.connect((sys.argv[1],7777))
except Exception as e:
    input("Erreur de connexion au serveur ! Appuyer sur n'importe quelle touche pour sortir")
    sys.exit()

while True:
    data = s.recv(1500)
    if data.decode("utf-8") == "J1" :
        whoIAm = "J1"
        break
    elif data.decode("utf-8") == "J2" :
        whoIAm = "J2"
        break

ACK = bytearray("ACK","utf-8")
s.send(ACK)
print("Vous êtes", whoIAm)

#Partie Joueur
if whoIAm != "spectator" :
    while grid.gameOver() == -1 :
       pass
#Partie spectateur
else :
    pass
#s.close()
