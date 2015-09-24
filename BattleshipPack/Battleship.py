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
opBoard.append("c")

#create user's board in the same fashion
myBoard = [['0' for x in range(10)] for y in range(10)]
myBoard.append("u")

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
my_ships_dict = {'b':4, 'd': 4, 's': 3, 'p': 2,'c':5}
op_ships_dict = {'b':4, 'd': 4, 's': 3, 'p': 2,'c':5}
ships_list = ['Battleship', "Destroyer", "Submarine", "Patrol Boat", "Carrier"]

#********************************************************************************
#printMenu() - prints out the name of the game
#
#pre - none
#post - menu has been printed
#********************************************************************************

def printMenu():
    print "    ____            __  __          __                   "
    print "   / __ )___  _____/ /_/ /__  _____/ /_  ___  _________  "
    print "  / __  / _ \/ ___/ __/ / _ \/ ___/ __ \/ _ \/ ___/ __ \ "
    print " / /_/ /  __/ /  / /_/ /  __(__  ) / / /  __/ /  / /_/ / "
    print "/_____/\___/_/   \__/_/\___/____/_/ /_/\___/_/  / .___/  "
    print "                                               /_/       "
    print
    inpoo = raw_input("Welcome to Bertlesherp! Press 'M' to manually deploy your "
                      "ships or 'A' to have your ships automatically deployed: ")

    while inpoo.upper() != 'A' and inpoo.upper() != 'M':
        inpoo = raw_input("Invalid character! Please select 'A' or 'M': ")

    if inpoo.upper() == 'A':
        return True
    else:
        return False


#********************************************************************************
#printBoard(board) - prints out the inputted board
#
#pre - an array with an identification letter is passed into the function
#post - the board has been printed with identification, dividers, and coordinates
#********************************************************************************

def printBoard(board):

    #checks identification character to determine which name to print out
    if board[len(board)-1] == 'u':
        print "User's board:\n"
    else:
        print "Computer's board:\n"

    #print out the top row of numbers using the letterspos dictionary
    print " ",
    for letter in alphabet:
        print "   " + str(letterspos[letter]) + " ",
    print

    #for the player's board...
    if board[len(board)-1] == "u":

        #print the divising line and the letter coordinate for that line from the
        #alphabet dictionary for every row in the board, excluding the ID line
        for y in range(len(board)-1):
            print "   -----------------------------------------------------------"
            print alphabet[y].upper(),

            #for every location on the board, if it's empty, print a blank space
            #if not, print what is at that location
            for x in range(len(board[y])):
                if board[y][x] == '0':
                    print "|    ",
                else:
                    print "|  " + board[y][x] + " ",
            print

    else:

        for y in range(len(board)-1):
            print "   -----------------------------------------------------------"
            print alphabet[y].upper(),

            for x in range(len(board[y])):
                if board[y][x] == 'M':
                    print "|  M ",
                elif board[y][x] == '*':
                    print "|  * ",
                else:
                    print "|    ",
            print

#********************************************************************************
#get_user_input_loc() - prompts the user for a location in coordinates
#
#pre - none
#post - valid coordinate points have been parsed and returned
#********************************************************************************

def get_user_input_loc():

    #take user input as a string
    inp = str(raw_input("Enter letter and number: "))

    #data validation to check if the first item is a valid character and the
    #second item is a valid number on the board
    while inp[0].lower() not in letterspos or int(inp[2:len(inp)]) > 10:
        print "Please choose a letter and number from the board"
        inp = str(raw_input("Enter letter and number: "))

    #save input to variables and return them as coordinates, making appropriate
    #compensation for the 0-start nature of the array and the first ID row
    row = letterspos[inp[0].lower()]
    col = int(inp[2:len(inp)])

    return row-1, col-1


def get_user_input_orient():

    #takes user input
    inp = raw_input("Enter a direction (N, S, E, or W): ")

    #checks input for valid direction
    while inp.lower() != 'e' and inp != 's' and inp != 'n' and inp != 'w':
        inp = raw_input("Enter a valid direction (N, S, E, or W): ")

    return inp


def deployShips(board, autoornah):

    #if deployment is automatic...
    if autoornah:

        #generates a random number between 0 and 9 and a random direction from
        #the orientation list for the starting coordinate of each ship
        for x in ships_list:
            row, col = random.randint(0,9), random.randint(0,9)
            orient = random.choice(orientations)

            #data validation to check the boundaries and check for other ships
            while checkBoundaries(x[0].lower(), row, col, orient) == False or \
                            checkForShip(board, x[0].lower(), row, col, orient) == False:
                row, col = random.randint(0,9), random.randint(0,9)
                orient = random.choice(orientations)

            #once coordinates are good, place the ship
            place_ship(board, x[0].lower(), row, col, orient)

        #if it's the user's board, print the board
        if board[len(board)-1] == "u":
            printBoard(board)

    #if deployment is manual...
    else:

        #place each ship in the ship list
        for x in ships_list:

            #clear the screen and print the board
            os.system('cls' if os.name == 'nt' else 'clear')
            printBoard(board)

            #prompt to place each ship in the ship list with number of spaces allowed
            print "Place your " + x + "(" + str(my_ships_dict[x[0].lower()]) + "):"

            #call user input functions
            row, col = get_user_input_loc()
            orient = get_user_input_orient()

            #data validation to check boundaries and check for other ships
            while checkBoundaries(x[0].lower(), row, col, orient) == False or \
                            checkForShip(board, x[0].lower(), row, col, orient) == False:
                print "Please place your ship within the board where it does not overlap another ship"
                row, col = get_user_input_loc()
                orient = get_user_input_orient()

            #when coordinates are good, place the ship
            place_ship(board, x[0].lower(), row, col, orient)

        #since manual deployment is always user based, print the board
        printBoard(board)


def place_ship(board, ship, row, col, orient):

    #for the length of the ship as defined in the dictionary...
    for x in range(my_ships_dict[ship]):

        #for each direction, place the letter of that ship in every
        #space along that direction with compensation for the ID row
        if orient == 's':
            board[row + x][col] = ship.upper()

        elif orient == 'e':
            board[row][col + x] = ship.upper()

        elif orient == 'n':
            board[row - x][col] = ship.upper()

        else: 
            board[row][col - x] = ship.upper()


def checkForShip(board, ship, row, col, orient):

    #for each orientation and for every space of the ship, check if that position
    #is currently occupied and return false if it is
    if orient == 's':
        for x in range(my_ships_dict[ship]):
            if check_position(board, row + x, col) == False:
                return False
    elif orient == 'e':
        for x in range(my_ships_dict[ship]):
            if check_position(board, row, col + x) == False:
                return False
    elif orient == 'n':
        for x in range(my_ships_dict[ship]):
            if check_position(board, row - x, col) == False:
                return False
    else: 
        for x in range(my_ships_dict[ship]):
            if check_position(board, row, col - x) == False:
                return False


def check_position(board, row, col):
    if board[row][col] != '0':
        return False

def checkBoundaries(ship, row, col, orient):
    if orient == 's':
        for x in range(my_ships_dict[ship]):
            if (row + x) > 9:
                return False
    elif orient == 'e':
        for x in range(my_ships_dict[ship]):
            if (col + x) > 9:
                return False
    elif orient == 'n':
        for x in range(my_ships_dict[ship]):
            if (row - x) < 0:
                return False
    else:
        for x in range(my_ships_dict[ship]):
            if (col - x) < 0:
                return False


def check_hit(board, row, col):
    for x in ships_list:
        if board[row][col] == x[0]:
            if board[len(board)-1] == 'u':
                my_ships_dict[x[0].lower()] -= 1
            else:
                op_ships_dict[x[0].lower()] -= 1
            return True
    return False

def check_fired(board, row, col):
    if board[row][col] == '*' or board[row][col] == 'M':
        return False
    else:
        return True


def main():

    autoornah = printMenu()

    deployShips(myBoard, autoornah)

    print "All ships deployed"
    print "Computer deploying ships..."

    deployShips(opBoard, True)

    print "Computer ships deployed"

    printBoard(opBoard)
    myShipsLeft = 5
    opShipsLeft = 5

    while (myShipsLeft > 0 and opShipsLeft > 0):
        print "Fire at your opponent! ",
        locx, locy = get_user_input_loc()
        while check_fired(opBoard, locx, locy) == False:
            print "Youve already shot there. Try again. "
            locx, locy = get_user_input_loc()
        if check_hit(opBoard, locx, locy) == True:
            print "HIT!!!!!!!!!!!!!!!!!!!!!!!!"








main()

