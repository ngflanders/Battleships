'''
Created on Sep 21, 2015

@author: Nick Flanders, Nicole Gerber
'''

#import libraries
import os
import time
import random

#create opponent's (computer's) board by making an array and adding a "c" to the top
#for identification
opBoard = [['0' for x in range(10)] for y in range(10)]
opBoard.insert(0, "c")

#create user's board in the same fashion
myBoard = [['0' for x in range(10)] for y in range(10)]
myBoard.insert(0, "u")

#variables for each ship with how many lives they have
bship = 4
destroyer = 4
sub = 3
patrol = 2
carrier = 5

#lists and dictionaries for the ships, lives, board positions, and orientations
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
orientations = ['n', 's', 'e', 'w']
letterspos = {'a': 0, 'b': 1, 'c':2, 'd':3, 'e':4,'f':5,'g':6,'h':7, 'i': 8, 'j': 9}
ships_dict = {'b':4, 'd': 4, 's': 3, 'p': 2,'c':5}
ships_list = ['Battleship', "Destroyer", "Submarine", "Patrol Boat", "Carrier"]

#********************************************************************************
#printMenu() - prints out the name of the game
#
#pre - none
#post - menu has been printed
#********************************************************************************

def printMenu():
    print "    ____            __  __          __                        "
    print "   / __ )___  _____/ /_/ /__  _____/ /_  ___  _________  _____"
    print "  / __  / _ \/ ___/ __/ / _ \/ ___/ __ \/ _ \/ ___/ __ \/ ___/"
    print " / /_/ /  __/ /  / /_/ /  __(__  ) / / /  __/ /  / /_/ (__  ) "
    print "/_____/\___/_/   \__/_/\___/____/_/ /_/\___/_/  / .___/____/  "
    print "                                               /_/            "
    print

#********************************************************************************
#printBoard() - prints out the inputted board
#
#pre - an array with an identification letter is passed into the function
#post - the board has been printed with identification, dividers, and coordinates
#********************************************************************************

def printBoard(board):
    if board[0] == 'u':
        print "User's board:\n"
    else:
        print "Computer's board:\n"

    print " ",
    for letter in alphabet:
        print "   " + str(letterspos[letter]+1) + " ",
    print
    if board[0] == "u":
        for y in range(1, 11):
            print "   -----------------------------------------------------------"
            print alphabet[y-1].upper(),
            for x in range(len(board[y])):
                if board[y][x] == '0':
                    print "|    ",
                else:
                    print "|  " + board[y][x] + " ",
            print

#********************************************************************************
#get_user_input_loc() - prompts the user for a location in coordinates
#
#pre - none
#post - valid coordinate points have been parsed and returned
#********************************************************************************

def get_user_input_loc():
    inp = str(raw_input("Enter letter and number: "))

    while inp[0].lower() not in letterspos or int(inp[2:len(inp)]) > 10:
        print "Please choose a letter and number from the board"
        inp = str(raw_input("Enter letter and number: "))
    
    row = letterspos[inp[0].lower()]
    col = int(inp[2:len(inp)])

    return row, col-1


def get_user_input_orient():
    inp = raw_input("Enter a direction (N, S, E, or W): ")
    while inp != 'e' and inp != 's' and inp != 'n' and inp != 'w':
        inp = raw_input("Enter a valid direction (N, S, E, or W): ")
    return inp


def deployShips(board, autoornah):
    if autoornah:
        for x in ships_list:
            row, col = random.randint(0,9), random.randint(0,9)
            orient = random.choice(orientations)

            while checkBoundaries(x[0].lower(), row, col, orient) == False or checkForShip(board, x[0].lower(), row, col, orient) == False:
                row, col = random.randint(0,9), random.randint(0,9)
                orient = random.choice(orientations)


            place_ship(board, x[0].lower(), row, col, orient)
        if board[0] == "u":
            printBoard(board)
    else:
        for x in ships_list:
            os.system('cls' if os.name == 'nt' else 'clear')
            printBoard(board)

            print "Place your " + x + "(" + str(ships_dict[x[0].lower()]) + "):"
            row, col = get_user_input_loc()
            orient = get_user_input_orient()

            while checkBoundaries(x[0].lower(), row, col, orient) == False or checkForShip(board, x[0].lower(), row, col, orient) == False:
                print "Please place your ship within the board where it does not overlap another ship"
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
            board[row - x + 1][col] = ship.upper()
        else: 
            board[row + 1][col - x] = ship.upper()


def checkForShip(board, ship, row, col, orient):
    if orient == 's':
        for x in range(ships_dict[ship]):
            if check_position(board, row + x +1, col) == False:
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


def check_position(board, row, col):
    if board[row][col] != '0':
        return False

def checkBoundaries(ship, row, col, orient):
    if orient == 's':
        for x in range(ships_dict[ship]):
            if (row + x) > 9:
                return False
    elif orient == 'e':
        for x in range(ships_dict[ship]):
            if (col + x) > 9:
                return False
    elif orient == 'n':
        for x in range(ships_dict[ship]):
            if (row - x) < 0:
                return False
    else:
        for x in range(ships_dict[ship]):
            if (col - x) < 0:
                return False
    

def check_fired(board, row, col):
    if board[col][row] == '*' or board[col][row] == 'M':
        return False
    else:
        return True


def main():
    printMenu()
    inpoo = raw_input("Would you like to deploy your own ships or have them auto deployed? T for auto, F for manual: ")
    if inpoo == 'T':
        autoornah = True
    else:
        autoornah = False

    deployShips(myBoard, autoornah)

    print "All ships deployed"
    print "Computer deploying ships..."

    deployShips(opBoard, True)

    print "Computer ships deployed"

    myShipsLeft = 5
    opShipsLeft = 5

    while (myShipsLeft > 0 and opShipsLeft > 0):
        print "Fire at your opponent! ",
        locx, locy = get_user_input_loc()
        while check_fired(opBoard, locx, locy) == False:
            locx, locy = get_user_input_loc()







main()

