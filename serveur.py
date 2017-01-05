#!/usr/bin/env python3
import socket
import select
import threading
import binascii
from grid import *
import os

def sendAgain(s, position):
    global again
    s.send(again)
    answer = s.recv(1500)
    if answer.decode("utf-8") == "NO" :
        global l
        del l[position]
        nbPlayer -= 1

def sendShot(otherS):
    global shotPlayed
    if shotPlayed : 
        global whoPayed
        otherS.send(bytearray("SHOT", "utf-8"))
        msg = otherS.recv(1500)
        for shot in shotPlayed :
            otherS.send(bytearray(shot, "utf-8"))
            msg = otherS.recv(1500)
        otherS.send(bytearray("END", "utf-8"))
        data = otherS.recv(1500)
        for player in whoPayed :
            otherS.send(bytearray(str(player), "utf-8"))
            data = otherS.recv(1500)
        otherS.send(bytearray("ENDOFEND", "utf-8"))  
        data = otherS.recv(1500)
        global current_player
        otherS.send(bytearray(str(current_player), "utf-8")) 

#Fonction permettant de recevoir un accusé de réception de la part d'un joueur
def ACK(player):
    while True:
        global l
        ACK = l[player].recv(1500)
        if ACK.decode("utf-8") == "ACK":
            break;

#Fonction qui permet d'effectuer les connexions (thread)
def connect():
    while True:
        lSocket = select.select(l,[],[])[0]
        for newS in lSocket:
            global s
            if s == newS :
                global nbPlayer
                nbPlayer += 1
                otherS, addr = newS.accept()
                global l
                l.append(otherS)
                if nbPlayer > 2 :
                    msg = bytearray("spectator", "utf-8")
                    otherS.send(msg)
                    tmp = otherS.recv(1500)
                    sendShot(otherS)
                    if winTest1 :
                        global win1
                        otherS.send(win1)
                    if winTest2 :
                        global win2
                        otherS.send(win2)
                    if winDraw :
                        global draw
                        otherS.send(draw)
                        

nbPlayer = 0

winTest1 = False
winTest2 = False
winDraw = False

inGame = False
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM,0)
l = []
shotPlayed = []
whoPayed = []
grid = grid() # Une seule grille logique

#MAIN
i=0
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
s.bind(('localhost',7777))
s.listen(1)
l.append(s)
os.system('clear')
print("En attente de joueurs...")
threading.Thread(None,connect,None).start()
while True :
    if nbPlayer >= 2 and inGame == False :
        os.system('clear')
        print("Début d'une partie")
        inGame = True
        #Envoie du premier msg => définit J1
        b = bytearray("J1","utf-8")
        l[1].send(b)
        b = bytearray("J2","utf-8")
        l[2].send(b)

        #Accusé de reception
        while True :
            ACK_J1 = l[1].recv(1500)
            ACK_J2 = l[2].recv(1500)
            if ACK_J1.decode("utf-8") == "ACK" :
                J1_OK = True
            if ACK_J2.decode("utf-8") == "ACK" :
                J2_OK = True
            if J1_OK == True and J2_OK == True :
                break;

        #Partie Jeu
        current_player = 1
        while grid.gameOver() == -1 :
            play = bytearray("PLAY", "utf-8")
            l[current_player].send(play)
            data = l[current_player].recv(5000)
            if not data : break
            elif data.decode("utf-8") == "ACK" :
                data = l[current_player].recv(5000)
            shot = int(data.decode("utf-8"))
            if grid.cells[shot] != 0 :
                answer = bytearray("NO", "utf-8")
                l[current_player].send(answer)
                ACK(current_player)
                l[current_player].send(play)
            else:
                answer = bytearray("YES", "utf-8")
                shotPlayed.append(data.decode("utf-8"))
                whoPayed.append(current_player)
                l[current_player].send(answer)
                grid.play(current_player, shot)
                shotMsg = bytearray(data.decode("utf-8"), "utf-8")
                os.system('clear')
                grid.display()
                ACK(current_player)
                for i in range(3, nbPlayer+1):
                    l[i].send(shotMsg)
                current_player = current_player%2+1

        print("Partie Finie")
        win = bytearray("WIN", "utf-8")
        win1 = bytearray("WIN1", "utf-8")
        win2 = bytearray("WIN2", "utf-8")
        loose = bytearray("LOOSE", "utf-8")
        draw = bytearray("DRAW", "utf-8")
        if grid.gameOver() == 1:
            winTest1 = True
            l[1].send(win)
            l[2].send(loose)
            for i in range(3, nbPlayer+1):
                l[i].send(win1)
        elif grid.gameOver() == 2:
            winTest2 = True
            l[2].send(win)
            l[1].send(loose)
            for i in range(3, nbPlayer+1):
                l[i].send(win2)
        else :
            winDraw = True
            for i in range(1, nbPlayer+1):
                l[i].send(draw)
        sendShot(l[1])
        sendShot(l[2]) 

        again = bytearray("AGAIN", "utf-8")
        thread = []
        for i in range(1, nbPlayer):
            print("Joueur" ,i)
            thread.append(threading.Thread(None,sendAgain,l[i],i,None))
            thread[i].start()
        for i in range(1, nbPlayer):
            thread[i].join()