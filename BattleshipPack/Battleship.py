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


import os
import time
import random

# create opponent's (computer's) board by making an array and adding a "c" to the top
# for identification
opBoard = [['0' for x in range(10)] for y in range(10)]
opBoard.append("c")

# create user's board in the same fashion
myBoard = [['0' for x in range(10)] for y in range(10)]
myBoard.append("u")

# list of valid alphabet letters for the board
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

# list of valid orientations
orientations = ['n', 's', 'e', 'w']

# dictionary of letters and their corresponding board locations
letterspos = {'a': 0, 'b': 1, 'c':2, 'd':3, 'e':4,'f':5,'g':6,'h':7, 'i': 8, 'j': 9}

# dictionaries to hold the number of lives for each ship
my_ships_dict = {'b':4, 'd': 4, 's': 3, 'p': 2,'c':5}
op_ships_dict = {'b':4, 'd': 4, 's': 3, 'p': 2,'c':5}

# list of full ship names
ships_list = ['Battleship', "Destroyer", "Submarine", "Patrol Boat", "Carrier"]

# variables to hold how many ships are left
myShipsLeft = 5
opShipsLeft = 5

# empty list to hold possible firing locations for smart AI
opAttackList = []


#********************************************************************************
# printMenu() - prints out the name of the game
#
# pre - none
# post - menu has been printed
#********************************************************************************
def printMenu():

    # display
    print "    ____        __  __  __          __    _      "
    print "   / __ )____ _/ /_/ /_/ /__  _____/ /_  (_)___  "
    print "  / __  / __ `/ __/ __/ / _ \/ ___/ __ \/ / __ \ "
    print " / /_/ / /_/ / /_/ /_/ /  __(__  ) / / / / /_/ / "
    print "/_____/\__,_/\__/\__/_/\___/____/_/ /_/_/ .___/  "
    print "                                       /_/       "
    print

    # welcome message and prompt for easy or hard mode
    mode = raw_input("Welcome to Battleship! Press 'E' for easy mode and 'H' for "
                      "hard mode: ")

    #data validation
    while mode.upper() != 'E' and mode.upper() != 'H':
        mode = raw_input("Invalid input! Please select 'E' or 'H': ")

    # sets easy_mode variable based on user input
    if mode.upper() == 'E':
        easy_mode = True
    else:
        easy_mode = False

    # prompt for auto/manual deployment
    deploy = raw_input("Press 'M' to manually deploy your "
                      "ships or 'A' to have your ships automatically deployed: ")

    # data validation
    while deploy.upper() != 'A' and deploy.upper() != 'M':
        deploy = raw_input("Invalid character! Please select 'A' or 'M': ")

    # sets auto_deploy variable based on user input
    if deploy.upper() == 'A':
        auto_deploy =  True
    else:
        auto_deploy = False

    return easy_mode, auto_deploy


#********************************************************************************
# simpleBoard(board) - prints out the inputted board in a simple form for testing
#
# pre - an array with an identification letter is passed into the function
# post - a simple board has been printed with all symbols shown
#********************************************************************************
def simpleBoard(board):

    # identification check to print header
    if board[len(board)-1] == 'u':
        print "User's board:\n"
    else:
        print "Computer's board:\n"

    # for every coordinate in the array, print what is at that location
    for y in range(len(board)-1):
        for x in range(len(board[y])):
            print board[y][x] + " ",
        print
    print


#********************************************************************************
# printPlayerBoard() - prints out the player's board
#
# pre - myBoard has been initialized
# post - the player's board has been printed with ID, dividers, and coordinates,
#       along with all of the ships on the board
#********************************************************************************
def printPlayerBoard():

    cls()
    print "Player's board:\n"

    # print out the top row of numbers using the letterspos dictionary
    print " ",
    for letter in alphabet:
        print "   " + str(letterspos[letter]+1) + " ",
    print

    # print the divising line and the letter coordinate for that line from the
    # alphabet dictionary for every row in the board, excluding the ID line
    for y in range(len(myBoard)-1):
        print "   -----------------------------------------------------------"
        print alphabet[y].upper(),

        # for every location on the board, if it's empty, print a blank space
        # if not, print what is at that location
        for x in range(len(myBoard[y])):
            if myBoard[y][x] == '0':
                print "|    ",
            else:
                print "|  " + myBoard[y][x] + " ",
        print
    print


#********************************************************************************
# printComputerBoard() - prints out the computer's board
#
# pre - opBoard has been initialized
# post - the computer's board has been printed with ID, dividers, and coordinates,
#       with no ships visible, only hits and misses
#********************************************************************************
def printComputerBoard():

    cls()
    print "Computer's board:\n"

    # print out the top row of numbers using the letterspos dictionary
    print " ",
    for letter in alphabet:
        print "   " + str(letterspos[letter]+1) + " ",
    print

    # print the divising line and the letter coordinate for that line from the
    # alphabet dictionary for every row in the board, excluding the ID line
    for y in range(len(opBoard)-1):
        print "   -----------------------------------------------------------"
        print alphabet[y].upper(),

        # for every location on the board, only print hits and misses
        for x in range(len(opBoard[y])):
            if opBoard[y][x] == '-':
                print "|  - ",
            elif opBoard[y][x] == '*':
                print "|  * ",
            else:
                print "|    ",
        print
    print


#********************************************************************************
# printBoard(board) - prints out the inputted board
#
# pre - an array with an identification letter is passed into the function
# post - the selected board has been printed
#********************************************************************************
def printBoard(board):

    # checks identification character to determine which name to print out and
    # calls the appropriate function to print the selected board
    if board[len(board)-1] == 'u':
        printPlayerBoard()
    else:
        printComputerBoard()


#********************************************************************************
# getUserInputLoc() - prompts the user for a location in coordinates
#
# pre - none
# post - valid coordinate points have been parsed and returned
#********************************************************************************
def getUserInputLoc():

    # take user input as a string
    inp = str(raw_input("Enter letter and number (separated by a space): "))

    # data validation to check if the first item is a valid character and the
    # second item is a valid number on the board
    while True:
        try:
            num = int(inp[2:len(inp)])
            if inp[0].lower() not in letterspos:
                # raises our choice of error
                raise NameError("Letter")
            if num > 10 or num < 1:
                # raises our choice of error
                raise NameError("Num")
            # breaks out of loop if no errors are raised
            break

        # handles the exceptions, and allows user to re-input
        except ValueError:
            print "Invalid format. Try again. "
            inp = str(raw_input("Enter letter and number (separated by a space): "))
        except NameError:
            print "Something is wrong. Either your letter or number is out of bounds"
            inp = str(raw_input("Enter letter and number (separated by a space): "))


    # save input to variables and return them as coordinates, making appropriate
    # compensation for the 0-start nature of the array
    row = letterspos[inp[0].lower()]
    col = int(inp[2:len(inp)])


    # letterspos naturally returns the correct value of the array, but the column
    # that the user inputted must be decremented
    return row, col-1


#********************************************************************************
# getUserInputOrient() - prompts the user for an orientation
#
# pre - none
# post - a valid orientation has been returned
#********************************************************************************
def getUserInputOrient():

    # takes user input
    inp = raw_input("Enter a direction (N, S, E, or W): ")

    # checks input for valid direction
    while inp.lower() != 'e' and inp != 's' and inp != 'n' and inp != 'w':
        inp = raw_input("Enter a valid direction (N, S, E, or W): ")

    return inp


#********************************************************************************
# autoDeploy(board) - automatically deploys the ships on the given board
#
# pre - none
# post - ships have been placed in valid locations in random positions
#********************************************************************************
def autoDeploy(board):

    # generates a random number between 0 and 9 and a random direction from
    # the orientation list for the starting coordinate of each ship
    for ship_name in ships_list:
        row, col = random.randint(0,9), random.randint(0,9)
        orient = random.choice(orientations)

        # data validation to check the boundaries and check for other ships
        while checkBoundaries(ship_name[0].lower(), row, col, orient) == False or \
                        checkForShip(board, ship_name[0].lower(), row, col, orient) == False:
            row, col = random.randint(0,9), random.randint(0,9)
            orient = random.choice(orientations)

        # once coordinates are good, place the ship
        placeShip(board, ship_name[0].lower(), row, col, orient)


#********************************************************************************
# manualDeploy(board) - places ships in inputted locations
#
# pre - none
# post - ships have been placed in valid locations from user input
#********************************************************************************
def manualDeploy(board):

    # place each ship in the ship list
    for ship_name in ships_list:

        # print the board
        printBoard(board)

        # prompt to place each ship in the ship list with number of spaces allowed
        print "Place your " + ship_name + "(" + str(my_ships_dict[ship_name[0].lower()]) + "):"

        # call user input functions
        row, col = getUserInputLoc()
        orient = getUserInputOrient()

        # data validation to check boundaries and check for other ships
        while checkBoundaries(ship_name[0].lower(), row, col, orient) == False or \
                        checkForShip(board, ship_name[0].lower(), row, col, orient) == False:
            print "Please place your ship within the board where it does not overlap another ship"
            row, col = getUserInputLoc()
            orient = getUserInputOrient()

        # when coordinates are good, place the ship
        placeShip(board, ship_name[0].lower(), row, col, orient)


#********************************************************************************
# deployShips(board, autoornah) - deploys ships automatically or manually
#
# pre - none
# post - the appropriate deploy function has been called based on whether the
#        calling function requested automatic or manual
#********************************************************************************
def deployShips(board, autoornah):

    # if deployment is automatic...
    if autoornah:

        autoDeploy(board)

        # if it's the user's board, print the board
        if board[len(board)-1] == "u":
            printBoard(board)

    # if deployment is manual...
    else:

        manualDeploy(board)

        # since manual deployment is always user based, print the board
        printBoard(board)


#********************************************************************************
# placeShip(board, ship, row, col, orient) - places the given ship on the given
#                                            board at the given coordinates in the
#                                            given orientation
#
# pre - valid coordinates/orientation have been passed into the function
# post - the ship is placed
#********************************************************************************
def placeShip(board, ship, row, col, orient):

    # for the length of the ship as defined in the dictionary...
    for x in range(my_ships_dict[ship]):

        # for each direction, place the letter of that ship in every
        # space along that direction
        if orient == 's':
            board[row + x][col] = ship.upper()

        elif orient == 'e':
            board[row][col + x] = ship.upper()

        elif orient == 'n':
            board[row - x][col] = ship.upper()

        else:
            board[row][col - x] = ship.upper()


#********************************************************************************
# checkForShip(board, ship, row, col, orient) - checks if there are any ships in
#                                               the area before placing a ship
#
# pre - in-bound coordinates and orientation have been passed in
# post - true or false has been returned depending on whether there is a ship there
#********************************************************************************

def checkForShip(board, ship, row, col, orient):

    # for each orientation and for every space of the ship, check if that position
    # is currently occupied and return false if it is

    if orient == 's':
        for x in range(my_ships_dict[ship]):
            if checkPosition(board, row + x, col) == False:
                return False

    elif orient == 'e':
        for x in range(my_ships_dict[ship]):
            if checkPosition(board, row, col + x) == False:
                return False

    elif orient == 'n':
        for x in range(my_ships_dict[ship]):
            if checkPosition(board, row - x, col) == False:
                return False

    else:
        for x in range(my_ships_dict[ship]):
            if checkPosition(board, row, col - x) == False:
                return False


#********************************************************************************
# checkPosition(board, row, col) - checks if there is something at a given position
#
#
# pre - board has been initialized and valid row/col have been passed in
# post - false has been returned if there is a non-0 at the location given
#********************************************************************************
def checkPosition(board, row, col):

    # if the position selected on the board isn't 0, then there is something
    # at that location and it returns false
    if board[row][col] != '0':
        return False


#********************************************************************************
# checkBoundaries(ship, row, col, orient) - checks if the whole ship will fit at
#                                          the given coordinates
#
# pre - board has been initialized and valid row/col/orientation have been passed in
# post - false has been returned if a part of the ship will go out of bounds
#********************************************************************************
def checkBoundaries(ship, row, col, orient):

    # for each orientation and for every space of the ship, check if any part
    # of the ship is out of bounds if it is placed on the board
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


#********************************************************************************
# checkHit(board, row, col) - if there is a ship at the location fired at,
#                              put a '*' and decrement the lives of that ship,
#                              otherwise put a '-' for miss
#
# pre: valid board/row/col have been passed in
# post: the appropriate symbol has been placed on the board and the validity of
#       the shot has been returned
#********************************************************************************
def checkHit(board, row, col):

    #for every ship in the ships list...
    for ship_name in ships_list:

        #if the location fired at contains that ship...
        if board[row][col] == ship_name[0]:

            # turns the string into a list for manipulation, then change the value
            # then convert back to string
            temp = list(board[row][col])
            temp[0] = "*"
            board[row][col] = "".join(temp)

            # decrement the lives value of the ship for the inputted player
            if board[len(board)-1] == 'u':
                my_ships_dict[ship_name[0].lower()] -= 1

            else:
                op_ships_dict[ship_name[0].lower()] -= 1

            return True

    # if there were no ships at that location, it was a miss, turns the string
    # into a list for manipulation, then change the value then convert back to string
    temp = list(board[row][col])
    temp[0] = "-"
    board[row][col] = "".join(temp)
    return False


#********************************************************************************
# checkSunk(board) - returns a message if a ship was sunk
#
# pre: initialized board has been passed in
# post: A sunk message has been displayed if the ship was sunk
#********************************************************************************
def checkSunk(board):

    #for each ship in the list...
    for ship_name in ships_list:

        #for the user...
        if board[len(board)-1] == 'u':

            #if any of the ships has 0 lives left, display a sunk message, decrement
            #the number of ships left, and set the sunk ship to -1 as to not be
            #triggerd for being sunk again
            if my_ships_dict[ship_name[0].lower()] == 0:
                print "They sunk your " + ship_name
                global myShipsLeft
                myShipsLeft -= 1
                my_ships_dict[ship_name[0].lower()] -= 1

        #for the computer...
        else:

            #follows the same procedure as before
            if op_ships_dict[ship_name[0].lower()] == 0:
                print "You sunk their " + ship_name
                global opShipsLeft
                opShipsLeft -= 1
                op_ships_dict[ship_name[0].lower()] -= 1


#********************************************************************************
# checkFired(board, row, col) - returns if there has already been a shot there
#
# pre: initialized board and valid row/col have been passed in
# post: returns false if there is already a shot there, true if otherwise
#********************************************************************************
def checkFired(board, row, col):

    # if there is a hit/miss symbol at that location, it has already
    # been fired at and returns false
    if board[row][col] == '*' or board[row][col] == '-':
        return False
    else:
        return True


#********************************************************************************
# userTurn() - executes all of the
#
# pre: none
# post: screen has been cleared
#********************************************************************************
def userTurn():
    print "Fire at your opponent! ",
    locx, locy = getUserInputLoc()
    while checkFired(opBoard, locx, locy) == False:
        print "You've already shot there. Try again. "
        locx, locy = getUserInputLoc()
    if checkHit(opBoard, locx, locy) == True:
        printBoard(opBoard)
        print "You got a hit!"
        checkSunk(opBoard)
    else:
        printBoard(opBoard)
        print "You missed."


#********************************************************************************
# simpleOpTurn() - handles the opponent's moves for easy mode
#
# pre: easy mode has been selected by the user
# post:
#********************************************************************************
def simpleOpTurn():
    row, col = random.randint(0,9), random.randint(0,9)
    while checkFired(myBoard, row, col) == False:
        row, col = random.randint(0,9), random.randint(0,9)
    if checkHit(myBoard, row, col) == True:
        printBoard(myBoard)
        print "You've been hit!"
        checkSunk(myBoard)
    else:
        printBoard(myBoard)
        print "Your opponent missed."

#********************************************************************************
# cls() - clears the screen regardless of operating system type
#
# pre: none
# post: screen has been cleared
#********************************************************************************

def smartOpTurn():
    if len(opAttackList) == 0:
        row, col = random.randint(0,9), random.randint(0,9)
        while checkFired(myBoard, row, col) == False:
            row, col = random.randint(0,9), random.randint(0,9)
        if checkHit(myBoard, row, col) == True:
            if row+1 <= 9:
                opAttackList.append([row+1, col])
            if row-1 >= 0:
                opAttackList.append([row-1, col])
            if col+1 <= 9:
                opAttackList.append([row, col+1])
            if col-1 >= 0:
                opAttackList.append([row, col-1])
            printBoard(myBoard)
            print "You've been hit!"
            checkSunk(myBoard)
        else:
            printBoard(myBoard)
            print "Your opponent missed."
    else:
        row, col = opAttackList.pop(0)
        if checkHit(myBoard, row, col) == True:
            if row+1 <= 9 and checkFired(myBoard, row+1, col)==True \
                    and opAttackList.count([row+1, col]) == 0:
                opAttackList.append([row+1, col])
            if row-1 >= 0 and checkFired(myBoard, row-1, col)==True \
                    and opAttackList.count([row-1, col]) == 0:
                opAttackList.append([row-1, col])
            if col+1 <= 9 and checkFired(myBoard, row, col+1)==True \
                    and opAttackList.count([row, col+1]) == 0:
                opAttackList.append([row, col+1])
            if col-1 >= 0 and checkFired(myBoard, row, col-1)==True \
                    and opAttackList.count([row, col-1]) == 0:
                opAttackList.append([row, col-1])
            printBoard(myBoard)
            print "You've been hit!"
            checkSunk(myBoard)
        else:
            printBoard(myBoard)
            print "Your opponent missed."

#********************************************************************************
# cls() - clears the screen regardless of operating system type
#
# pre: none
# post: screen has been cleared
#********************************************************************************
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


#********************************************************************************
# main()- displays menu, deploys ships, and plays game
#
# pre: none
# post: Battleship game has been played
#********************************************************************************
def main():
    # printMenu returns decision of user to auto deploy or manual
    easymode, autoornah = printMenu()
    cls()
    # deploy user's ships based on deployment decision
    deployShips(myBoard, autoornah)

    # success message, computer deployment
    print "\nAll ships deployed"
    raw_input("Press enter to continue...")
    print "Computer deploying ships..."
    time.sleep(1)

    # deploy computer's ships automatically
    deployShips(opBoard, True)

    # success message
    print "Computer ships deployed\n"
    raw_input("Press enter to begin game!")

    # BEGIN GAME PLAY

    turns = 0


    while True:

        turns += 1

        # USER'S TURN

        #simpleBoard(opBoard) #remove comment to view computer's board for testing
        printBoard(opBoard)
        userTurn()
        raw_input("Press enter to continue...")

        if opShipsLeft == 0:
            break

        # OP'S TURN
        printBoard(myBoard)
        print "Computer firing..."
        time.sleep(1)
        if easymode:
            simpleOpTurn()
        else:
            smartOpTurn()
        raw_input("Press enter to continue...")

        if myShipsLeft == 0:
            break

    if myShipsLeft == 0:
        print "\nYou lost! The computer beat you in " + str(turns) + " turns!"
    else:
        print "\nYou won! You beat the computer in " + str(turns) + " turns!"
    # closing message
    print "Thanks for playing Battleship!"


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Call to run the main program
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__=='__main__':
    random.seed(time.time())
    cls()
    main()
    raw_input('Press ENTER to continue...')
    cls()
