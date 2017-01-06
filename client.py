#!/usr/bin/env python3
import socket
import select
import threading
from grid import *
from main import *
import sys
import os

def getShot(grid) :
    global s
    global ACK
    data = s.recv(1500)

    if data.decode("utf-8") == "SHOT":
        s.send(ACK)
        shotPlayed = []
        whoPlayed = []
        data = s.recv(1500)
        while data.decode("utf-8") != "END" :
            s.send(ACK)
            shotPlayed.append(int(data.decode("utf-8")))
            data = s.recv(1500)
        s.send(ACK)
        data = s.recv(1500)
        while data.decode("utf-8") != "ENDOFEND" :
            s.send(ACK)
            whoPlayed.append(int(data.decode("utf-8")))
            data = s.recv(1500)
        for i in range(0, len(shotPlayed)):
            grid.play(whoPlayed[i], shotPlayed[i])
        s.send(ACK)
        data = s.recv(1500)
        global current_player
        current_player = int(data.decode("utf-8"))

choix = 0
while choix != 1 and choix != 2 :
    os.system('clear')
    print("Bienvenue sur le morpion aveugle !")
    print("1 : Jouez en réseaux")
    print("2 : Jouez contre un ordi")
    try :
        choix = int(input("Choix ? "))
    except Exception as e:
        pass

if choix == 2:
    main()
else :
    whoIAm = "spectateur"
    gridGraphic = grid() #une grille graphique uniquement, la logique étant gérée sur le serveur
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    os.system('clear')
    connect = False
    while connect == False :
        serveur = input("Entrez le nom du serveur : ")
        try:
            s.connect((serveur,7777))
            print("Connecté au serveur de jeu...")
            connect = True
        except Exception as e:
            print("Erreur de connexion au serveur !")

    again = True
    while again == True : 
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
        if whoIAm != "spectateur" :
            gridGraphic.display()
            data = s.recv(1500)
            while data.decode("utf-8") != "WIN" and data.decode("utf-8") != "DRAW" and data.decode("utf-8") != "LOOSE" :
                #Partie Jeu
                if data.decode("utf-8") == "PLAY" :
                    shotMsg = ''
                    while shotMsg == '' :
                        shotMsg = input ("Quelle case voulez-vous jouer ?")
                    shot = int(shotMsg)
                    if shot < 9 and shot > -1 :
                        envoiShot = bytearray(shotMsg , "utf-8")
                        s.send(envoiShot)
                        while True :
                            data = s.recv(1500)
                            if data.decode("utf-8") == "YES" :
                                os.system('clear')
                                if whoIAm == "J1":
                                    gridGraphic.play(1, shot)
                                    gridGraphic.display()
                                    s.send(ACK)
                                    break
                                else:
                                    gridGraphic.play(2, shot)
                                    gridGraphic.display()
                                    s.send(ACK)
                                    break
                            elif data.decode("utf-8") == "NO":
                                s.send(ACK)
                                break

                        data = s.recv(1500)

            #Fin de la partie
            os.system('clear')
            print("Partie finie")
            if data.decode("utf-8") == "WIN" :
                print("Vous avez gagné !")
            elif data.decode("utf-8") == "LOOSE" :
                print("Vous avez perdu !")
            elif data.decode("utf-8") == "DRAW" :
                print("Match nul !")
            
            gridFinal = grid()
            getShot(gridFinal)
            gridFinal.display()

        #Partie spectateur
        else :
            #Récupération des coups déjà 
            current_player = 1
            getShot(gridGraphic)
            gridGraphic.display()
            data = s.recv(1500)
            while data.decode("utf-8") != "WIN1" and data.decode("utf-8") != "DRAW" and data.decode("utf-8") != "WIN2" :
                gridGraphic.play(current_player, int(data.decode("utf-8")))
                os.system('clear')
                gridGraphic.display()
                current_player = current_player%2+1
                data = s.recv(1500)

            #Fin de la partie
            print("Partie finie")
            if data.decode("utf-8") == "WIN1" :
                print("Le joueur 1 a gagné !")
            elif data.decode("utf-8") == "WIN2" :
                print("Le joueur 2 a gagné !")
            elif data.decode("utf-8") == "DRAW" :
                print("Match nul !")

        data = s.recv(1500)
        again = False
        if data.decode("utf-8") == "AGAIN" :
            choix = 0
            choixMsg = ""
            while choix != 1 and choix != 2 :
                print("Voulez vous recommencer une partie ?")
                print("1 : Oui")
                print("2 : Non")
                choixMsg = input("Choix : ")
                try :
                    choix = int(choixMsg)
                except Exception as e:
                    pass
            if choix == 1 :
                choixEnvoi = bytearray("YES", "utf-8")
                again = True
                s.send(choixEnvoi)
                gridFinal = grid()
                gridGraphic = grid()
            else :
                choixEnvoi = bytearray("NO", "utf-8")
                s.send(choixEnvoi)
                s.close()