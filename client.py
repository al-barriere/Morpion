#!/usr/bin/env python3
import socket
import select
import threading
from grid import *
import sys
import os

os.system('clear')
whoIAm = "spectateur"
grid = grid() #une grille graphique uniquement, la logique étant gérée sur le serveur
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

try:
    s.connect((sys.argv[1],7777))
    print("Connecté au serveur de jeu...")
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
    elif data.decode("utf-8") == "spectator" :
        break
os.system('clear')
ACK = bytearray("ACK","utf-8")
s.send(ACK)
print("Vous êtes", whoIAm)

#Partie Joueur
grid.display()
if whoIAm != "spectateur" :
    data = s.recv(1500)
    while data.decode("utf-8") != "WIN" or data.decode("utf-8") != "DRAW" or data.decode("utf-8") != "LOOSE" :
        #Partie Jeu
        if data.decode("utf-8") == "PLAY" :
            shotMsg = input ("Quelle case voulez-vous jouer ?")
            shot = int(shotMsg)
            if shot < 9 or shot > -1 :
                envoiShot = bytearray(shotMsg , "utf-8")
                s.send(envoiShot)
                while True :
                    print("je suis la")
                    data = s.recv(1500)
                    if data.decode("utf-8") == "YES" :
                        os.system('clear')
                        if whoIAm == "J1":
                            grid.play(1, shot)
                            grid.display()
                            break
                        else:
                            grid.play(2, shot)
                            grid.display()
                            break
                    else:
                        break

                    s.send(ACK)
                    print("je suis la")
                    data = s.recv(1500)

    #Fin de la partie
    print("Partie fini")
    if data.decode("utf-8") != "WIN" :
        print("Vous avez gagné !")
    elif data.decode("utf-8") != "LOOSE" :
        print("Vous avez perdu !")
    elif data.decode("utf-8") != "DRAW" :
        print("Match nul !")


#Partie spectateur
else :
    grid.display()
    current_player = 1
    data = s.recv(1500)
    while data.decode("utf-8") != "WIN1" or data.decode("utf-8") != "DRAW" or data.decode("utf-8") != "WIN2" :
        grid.play(current_player, int(data.decode("utf-8")))
        os.system('clear')
        grid.display

    #Fin de la partie
    print("Partie fini")
    if data.decode("utf-8") != "WIN" :
        print("Vous avez gagné !")
    elif data.decode("utf-8") != "LOOSE" :
        print("Vous avez perdu !")
    elif data.decode("utf-8") != "DRAW" :
        print("Match nul !")


s.close()
