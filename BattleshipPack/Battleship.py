'''
Created on Sep 21, 2015

@author: Nick Flanders, Nicole Gerber
'''

import os
import time
import random

opBoard = [['0' for x in range(10)] for y in range(10)]
opBoard.insert(0, "c")
myBoard = [['0' for x in range(10)] for y in range(10)]
myBoard.insert(0, "u")

bship = 4
destroyer = 4
sub = 3
patrol = 2
carrier = 5

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
letterspos = {'a': 0, 'b': 1, 'c':2, 'd':3, 'e':4,'f':5,'g':6,'h':7, 'i': 8, 'j': 9}
ships_dict = {'b':4, 'd': 4, 's': 3, 'p': 2,'c':5}
ships_list = ['Battleship', "Destroyer", "Submarine", "Patrol Boat", "Carrier"]

def printBoard(board):
    print " ",
    for letter in alphabet:
        print "   " + str(letterspos[letter]+1) + " ",
    print
    if (board[0] == "u"):
        for y in range(1, 11):
            print "   -----------------------------------------------------------"
            print alphabet[y-1].upper(),
            for x in range(len(board[y])):
                print "|  " + board[y][x] + " ",
            print

def get_user_input_loc():
    inp = str(raw_input("Enter letter and number: "))

    while inp[0].lower() not in letterspos:
        print "Invalid letter. Try again."
        inp = str(raw_input("Enter letter and number: "))
    row = letterspos[inp[0].lower()]

    col = int(inp[2:len(inp)])
    while col > 10:
        print "Invalid number must be less than or equal to 10."
        col = int(raw_input("Enter a column number: "))

    return row, col-1


def get_user_input_orient():
    inp = raw_input("Enter a direction (N, S, E, or W): ")
    while inp != 'e' and inp != 's' and inp != 'n' and inp != 'w':
        inp = raw_input("Enter a valid direction (N, S, E, or W): ")
    return inp


def deployShips(board, autoornah):
    if autoornah:
        pass
    else:
        for x in ships_list:
            os.system('cls' if os.name == 'nt' else 'clear')
            printBoard(board)
            print "Place your " + x
            row, col = get_user_input_loc()
            orient = get_user_input_orient()
            while checkBoundaries(x[0].lower(), row, col, orient) == False:
                print "Out of bounds, brother..."
                row, col = get_user_input_loc()
                orient = get_user_input_orient()
            while checkForShip(board, x[0].lower(), row, col, orient) == False:
                print "Something's there, brother..."
                row, col = get_user_input_loc()
                orient = get_user_input_orient()
            place_ship(board, x[0].lower(), row, col, orient)
        printBoard(board)


def place_ship(board, ship, row, col, orient):
    for x in range(ships_dict[ship]):
        if orient == 's':
            board[row + x + 1][col] = ship.upper()
        elif orient == 'e':
            board[row + 1][col + x] = ship.upper()
        elif orient == 'n':
            board[row -x + 1][col] = ship.upper()
        else: 
            board[row + 1][col - x] = ship.upper()

def checkForShip(board, ship, row, col, orient):
    if orient == 's':
        for x in range(ships_dict[ship]):
            if board[row + x + 1][col] != '0':
                return False
    elif orient == 'e':
        for x in range(ships_dict[ship]):
            if board[row + 1][col + x] != '0':
                return False
    elif orient == 'n':
        for x in range(ships_dict[ship]):
            if board[row - x + 1][col] != '0':
                return False
    else: 
        for x in range(ships_dict[ship]):
            if board[row +1][col - x] != '0':
                return False

def checkBoundaries(ship, row, col, orient):
    if orient == 's':
        for x in range(ships_dict[ship]):
            if (row + x + 1) > 9:
                return False
    elif orient == 'e':
        for x in range(ships_dict[ship]):
            if (col + x) > 9:
                return False
    elif orient == 'n':
        for x in range(ships_dict[ship]):
            if (row - x + 1) < 0:
                return False
    else:
        for x in range(ships_dict[ship]):
            if (col - x) < 0:
                return False


#hey




#print get_user_input_loc()
#place_ship(myBoard, 'b', 2, 6, 'e')
#printBoard(myBoard)
deployShips(myBoard, False)
