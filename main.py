#!/usr/bin/python3

from grid import *
import  random
import os

def main():
    grids = [grid(), grid(), grid()]
    current_player = J1
    os.system('clear')
    grids[J1].display()
    while grids[0].gameOver() == -1:
        if current_player == J1:
            shot = -1
            while shot <0 or shot >=NB_CELLS:
                shot = int(input ("Quelle case allez-vous jouer ?"))
        else:
            shot = random.randint(0,8)
            while grids[current_player].cells[shot] != EMPTY:
                shot = random.randint(0,8)
        if (grids[0].cells[shot] != EMPTY):
            grids[current_player].cells[shot] = grids[0].cells[shot]
        else:
            grids[current_player].cells[shot] = current_player
            grids[0].play(current_player, shot)
            current_player = current_player%2+1
        if current_player == J1:
            os.system('clear')
            grids[J1].display()
    os.system('clear')
    print("Partie finie")
    grids[0].display()
    if grids[0].gameOver() == J1:
        print("Vous avez gagné !")
    else:
        print("Vous avez perdu !")
