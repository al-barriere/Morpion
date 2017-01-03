#!/usr/bin/env python3
import socket
import select
import threading
from grid import *
import os

def ACK(l, current_player):
    while True:
        ACK = l[current_player].recv[1500]
        if ACK.decode("utf-8") == "ACK":
            break;

nbPlayer = 0
inGame = False
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM,0)
l = []
clientAddr = []
grid = grid() # Une seule grille logique
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
                print(l)
                print(clientAddr)

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
    if nbPlayer >= 2 and inGame == False :
        print("Début d'une partie")
        inGame = True
        #Envoie du premier msg => définit J1
        b = bytearray("J1","utf-8")
        l[1].send(b)
        b = bytearray("J2","utf-8")
        l[2].send(b)

        #Accusé de reception
        while True :
            ACK_J1 = l[1].recv[1500]
            ACK_J2 = l[2].recv[1500]
            if ACK_J1.decode("utf-8") == "ACK" :
                J1_OK = True
            if ACK_J2.decode("utf-8") == "ACK" :
                J2_OK = True
            if J1_OK == True and J2_OK == True :
                break;

        #Partie Jeu
        current_player = 1
        while grid.gameOver() == -1 :
            data = l[current_player].recv(1500)
            if not data : break
            shot = int(data.decode("utf-8"))

            if grid.cells[shot] != 0 :
                answer = bytearray("NO", "utf-8")
                l[current_player].send(answer)
            else:
                answer = bytearray("YES", "utf-8")
                l[current_player].send(answer)
                grid.cells[shot] = current_player
                grid.play(current_player, shot)
                ACK(l, current_player)
                for i in range(3, nbPlayer): #Pensez à retirer un joueur s'il se déconnecte
                    l[i].send(data)
                current_player = current_player%2+1
                msg = bytearray("PLAY", "utf-8")
                l[current_player].send(msg)
                ACK(l, current_player)

        print("GAME OVER")
        win = bytearray("WIN")
        loose = bytearray("LOOSE")
        if grids[0].gameOver() == 1:
            l[1].send(win)
            l[2].send(loose)
        else:
            l[2].send(win)
            l[1].send(loose)
