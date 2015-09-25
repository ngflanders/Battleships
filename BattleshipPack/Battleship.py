'''
Battleship.py

Authors: Nick Flanders, Nicole Gerber
Course: CSCI 220
Date: 9/18/15
Description: This program, at the moment, prints a menu and allows the user to deploy their
             ships manually or automatically. Then, if they want to manually deploy their
             ships, prompts them to place each ship with proper data validation. If they
             chose automatic, their ships are automatically placed in random locations. Then,
             their board is printed and the computer's ships are deployed automatically. The
             computer's blank board is printed and then, after a pause, the simple boards
             showing all of the boards is printed.
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

    #display
    print "    ____            __  __          __                   "
    print "   / __ )___  _____/ /_/ /__  _____/ /_  ___  _________  "
    print "  / __  / _ \/ ___/ __/ / _ \/ ___/ __ \/ _ \/ ___/ __ \ "
    print " / /_/ /  __/ /  / /_/ /  __(__  ) / / /  __/ /  / /_/ / "
    print "/_____/\___/_/   \__/_/\___/____/_/ /_/\___/_/  / .___/  "
    print "                                               /_/       "
    print

    #welcome message and prompt for auto/manual deployment
    inpoo = raw_input("Welcome to Bertlesherp! Press 'M' to manually deploy your "
                      "ships or 'A' to have your ships automatically deployed: ")

    #data validation
    while inpoo.upper() != 'A' and inpoo.upper() != 'M':
        inpoo = raw_input("Invalid character! Please select 'A' or 'M': ")

    #returns the result of automatic or manual choice
    if inpoo.upper() == 'A':
        return True
    else:
        return False

#********************************************************************************
#simpleBoard(board) - prints out the inputted board in a simple form for testing
#
#pre - an array with an identification letter is passed into the function
#post - a simple board has been printed with all symbols shown
#********************************************************************************

def simpleBoard(board):

    #identification check to print header
    if board[len(board)-1] == 'u':
        print "User's board:\n"
    else:
        print "Computer's board:\n"

    #for every place in the array, print what is at that location
    for y in range(len(board)-1):
        for x in range(len(board[y])):
            print board[y][x] + " ",
        print
    print

#********************************************************************************
#printPlayerBoard() - prints out the player's board
#
#pre - myBoard has been initialized
#post - the player's board has been printed with ID, dividers, and coordinates,
#       along with all of the ships on the board
#********************************************************************************

def printPlayerBoard():

    print "Player's board:\n"

    #print out the top row of numbers using the letterspos dictionary
    print " ",
    for letter in alphabet:
        print "   " + str(letterspos[letter]+1) + " ",
    print

    #print the divising line and the letter coordinate for that line from the
    #alphabet dictionary for every row in the board, excluding the ID line
    for y in range(len(myBoard)-1):
        print "   -----------------------------------------------------------"
        print alphabet[y].upper(),

        #for every location on the board, if it's empty, print a blank space
        #if not, print what is at that location
        for x in range(len(myBoard[y])):
            if myBoard[y][x] == '0':
                print "|    ",
            else:
                print "|  " + myBoard[y][x] + " ",
        print

#********************************************************************************
#printComputerBoard() - prints out the computer's board
#
#pre - opBoard has been initialized
#post - the computer's board has been printed with ID, dividers, and coordinates,
#       with no ships visible, only hits and misses
#********************************************************************************

def printComputerBoard():

    print "Computer's board:\n"

    #print out the top row of numbers using the letterspos dictionary
    print " ",
    for letter in alphabet:
        print "   " + str(letterspos[letter]) + " ",
    print

    #print the divising line and the letter coordinate for that line from the
    #alphabet dictionary for every row in the board, excluding the ID line
    for y in range(len(opBoard)-1):
            print "   -----------------------------------------------------------"
            print alphabet[y].upper(),

            #for every location on the board, only print hits and misses
            for x in range(len(opBoard[y])):
                if opBoard[y][x] == 'M':
                    print "|  M ",
                elif opBoard[y][x] == '*':
                    print "|  * ",
                else:
                    print "|    ",
            print
    print



#********************************************************************************
#printBoard(board) - prints out the inputted board
#
#pre - an array with an identification letter is passed into the function
#post - the selected board has been printed
#********************************************************************************


def printBoard(board):

    #checks identification character to determine which name to print out and
    #calls the appropriate function to print the selected board
    if board[len(board)-1] == 'u':
        printPlayerBoard()
    else:
        printComputerBoard()



#********************************************************************************
#get_user_input_loc() - prompts the user for a location in coordinates
#
#pre - none
#post - valid coordinate points have been parsed and returned
#********************************************************************************

def get_user_input_loc():

    #take user input as a string
    inp = str(raw_input("Enter letter and number (separated by a space): "))

    #data validation to check if the first item is a valid character and the
    #second item is a valid number on the board
    while inp[0].lower() not in letterspos or int(inp[2:len(inp)]) > 10:
        print "Please choose a letter and number from the board"
        inp = str(raw_input("Enter letter and number (separated by a space): "))

    #save input to variables and return them as coordinates, making appropriate
    #compensation for the 0-start nature of the array
    row = letterspos[inp[0].lower()]
    col = int(inp[2:len(inp)])


    #letterspos naturally returns the correct value of the array, but the column
    #that the user inputted must be decremented
    return row, col-1

#********************************************************************************
#get_user_input_orient() - prompts the user for an orientation
#
#pre - none
#post - a valid orientation has been returned
#********************************************************************************

def get_user_input_orient():

    #takes user input
    inp = raw_input("Enter a direction (N, S, E, or W): ")

    #checks input for valid direction
    while inp.lower() != 'e' and inp != 's' and inp != 'n' and inp != 'w':
        inp = raw_input("Enter a valid direction (N, S, E, or W): ")

    return inp

#********************************************************************************
#autoDeploy(board) - automatically deploys the ships on the given board
#
#pre - none
#post - ships have been placed in valid locations in random positions
#********************************************************************************

def autoDeploy(board):

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

#********************************************************************************
#manualDeploy(board) - places ships in inputted locations
#
#pre - none
#post - ships have been placed in valid locations from user input
#********************************************************************************

def manualDeploy(board):

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



#********************************************************************************
#deployShips(board, autoornah) - deploys ships automatically or manually
#
#pre - none
#post - the appropriate deploy function has been called based on whether the
#       calling function requested automatic or manual
#********************************************************************************

def deployShips(board, autoornah):

    #if deployment is automatic...
    if autoornah:

        autoDeploy(board)

        #if it's the user's board, print the board
        if board[len(board)-1] == "u":
            printBoard(board)

    #if deployment is manual...
    else:

        manualDeploy(board)

        #since manual deployment is always user based, print the board
        os.system('cls' if os.name == 'nt' else 'clear')
        printBoard(board)

#********************************************************************************
#place_ship(board, ship, row, col, orient) - places the given ship on the given
#                                            board at the given coordinates in the
#                                            given orientation
#
#pre - valid coordinates/orientation have been passed into the function
#post - the ship is placed
#********************************************************************************

def place_ship(board, ship, row, col, orient):

    #for the length of the ship as defined in the dictionary...
    for x in range(my_ships_dict[ship]):

        #for each direction, place the letter of that ship in every
        #space along that direction
        if orient == 's':
            board[row + x][col] = ship.upper()

        elif orient == 'e':
            board[row][col + x] = ship.upper()

        elif orient == 'n':
            board[row - x][col] = ship.upper()

        else: 
            board[row][col - x] = ship.upper()

#********************************************************************************
#autoDeploy(board) - automatically deploys the ships on the given board
#
#pre - none
#post - ships have been placed in valid locations in random positions
#********************************************************************************

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

#********************************************************************************
#check_position(board, row, col) - checks if there is something at a given position
#
#pre - board has been initialized and valid row/col have been passed in
#post - false has been returned if there is a non-0 at the location given
#********************************************************************************

def check_position(board, row, col):

    #if the position selected on the board isn't 0, then there is something
    #at that location and it returns false
    if board[row][col] != '0':
        return False

#********************************************************************************
#checkBoundaries(ship, row, col, orient) - checks if the whole ship will fit at
#                                          the given coordinates
#
#pre - board has been initialized and valid row/col/orientation have been passed in
#post - false has been returned if a part of the ship will go out of bounds
#********************************************************************************

def checkBoundaries(ship, row, col, orient):

    #for each orientation and for every space of the ship, check if any part
    #of the ship is out of bounds if it is placed on the board
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

# def check_hit(board, row, col):
#
#     #Nick what is happening here???
#     for x in ships_list:
#         if board[row][col] == x[0]:
#             #board[row][col] = "*"
#             if board[len(board)-1] == 'u':
#                 my_ships_dict[x[0].lower()] -= 1
#             else:
#                 op_ships_dict[x[0].lower()] -= 1
#             return True
#    # temp = list(board[row][col])
#     #temp = "M"
#     #str(temp)
#     #board[row][col] = "M"
#     return False

# def check_fired(board, row, col):
#
#     #if there is a hit/miss symbol at that location, it has already
#     #been fired at and returns false
#     if board[row][col] == '*' or board[row][col] == 'M':
#         return False
#     else:
#         return True

# def check_fired(board, row, col):
#
#     #if there is a hit/miss symbol at that location, it has already
#     #been fired at and returns false
#     if board[row][col] == '*' or board[row][col] == 'M':
#         return False
#     else:
#         return True


def main():

    #printMenu returns decision of user to auto deploy or manual
    autoornah = printMenu()

    #deploy user's ships based on deployment decision
    deployShips(myBoard, autoornah)

    #success message, computer deployment
    print "\nAll ships deployed"
    print "Computer deploying ships..."

    #deploy computer's ships automatically
    deployShips(opBoard, True)

    #success message
    print "Computer ships deployed\n"

    #pause to view computer board
    raw_input("Press Enter to see simple boards...")

    #print the simple boards with all elements of array visible
    print "Simple boards:\n"

    simpleBoard(myBoard)
    simpleBoard(opBoard)

    #closing message
    print "Thanks for playing Bertlesherp!"

    # myShipsLeft = 5
    # opShipsLeft = 5
    #
    # while (myShipsLeft > 0 and opShipsLeft > 0):
    #     print "Fire at your opponent! ",
    #     locx, locy = get_user_input_loc()
    #     while check_fired(opBoard, locx, locy) == False:
    #         print "Youve already shot there. Try again. "
    #         locx, locy = get_user_input_loc()
    #     if check_hit(opBoard, locx, locy) == True:
    #         print "HIT!!!!!!!!!!!!!!!!!!!!!!!!"


    # deployShips(myBoard, True)
    # simpleBoard(myBoard)





main()

