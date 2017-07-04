"""
Noughts and Crosses
Ron Zhang, Kevin Kim
"""

from tkinter import *

mode = "Player vs Player"

#main function that will set up the window
def main():
    global canvas
    #Initialising window
    window = Tk()
    window.title("Noughts and Crosses")

    #Setting up the side frame
    sideFrame = Frame(window)

    #Setting up objects inside frame
    modeButton = Button(sideFrame, text="Change Mode", width=15, command=modeToggle)
    clearButton = Button(sideFrame, text="Clear", width=15, command=init)

    modeButton.pack()
    clearButton.pack()

    #Setting up the canvas
    canvas = Canvas(window, width=500, height=500, bg="#77eeff")

    #Packing things
    sideFrame.pack(side=RIGHT)
    canvas.pack(side=LEFT)

    #Drawing things in canvas
    init()

    window.mainloop()

#Function to draw and update the nessesary components
def init(event=None):
    global modeText, roundText, turnText, shapeX, shapeO

    clear()#Defining default variables

    #Establishing the grid inside the canvas - Border 10, Square width = 150, actual width = 140
    for y in range(3):
        for x in range(3):
            canvas.create_rectangle(
                                    25 + 150 * x, 25 + 150 * y,
                                    175 + 150 * x, 175 + 150 * y,
                                    width=10
                                    )

    #Creating the display text at the top
    modeText = canvas.create_text(20, 10, text="Mode = {}".format(mode), anchor=W)
    turnText = canvas.create_text(250, 10, text="Turn = {}".format(turn))
    roundText = canvas.create_text(480, 10, text="Round = {}".format(gameRound), anchor=E)


    #Drawing the shapes for the first time
    initCoords = [-100, -100, -100, -100]
    #Setting coords outside the canvas so that the variable exists, and can be modified later

    colour = "#53a6b2"
    shapeX = canvas.create_polygon(initCoords, fill=colour) #variable for the shape X
    shapeO = canvas.create_oval(initCoords, width="15", outline=colour) #variable for the shape Y

    #Binding the mouse
    canvas.bind("<Motion>", hoverLoc)
    canvas.bind("<Button-1>", clickLoc)

#Update display
def display():
    canvas.itemconfig(modeText, text="Mode = {}".format(mode))
    canvas.itemconfig(turnText, text="Turn = {}".format(turn))
    canvas.itemconfig(roundText, text="Round = {}".format(gameRound))

def modeToggle():
    global mode, canvas
    if mode == "Player vs Player":
        mode = "Player vs AI"
    elif mode == "Player vs AI":
        mode = "Player vs Player"

    display()

def clear():
    global turn, gameRound, gridShape
    turn = "x"
    gameRound = 0
    gridShape = [["","",""],["","",""],["","",""]]

    canvas.delete(ALL)

def hoverLoc(motion):
    #Defining x and y
    x = motion.x
    y = motion.y

    #Converting x and y into grid coords
    grid = gridCalc(x, y)

    #If mouse is inside a valid grid, and there are no previous inputs in that grid
    if grid != "MouseOutOfGrid" and gridShape[grid[1]][grid[0]] == "":
        coord = objectLoc(grid)#Defining the the coordinate of the object

        #moving object to position
        if turn == 'x':
            canvas.coords(shapeX, coord)
        elif turn == "o":
            canvas.coords(shapeO, coord)


def clickLoc(event):
    global turn, gameRound

    #Defining x and y coordinate of mouse
    x = event.x
    y = event.y

    #Translating the x y coords into grid coords
    grid = gridCalc(x, y)

    #If mouse is inside a valid grid, and there are no previous inputs in that grid
    if grid != "MouseOutOfGrid" and gridShape[grid[1]][grid[0]] == "":

        #translating grid coord to object coord
        coord = objectLoc(grid)

        #Adding one to round
        gameRound += 1

        if turn == "x":
            canvas.create_polygon(coord)
            gridShape[grid[1]][grid[0]] = "x"
            game = gameChecker(grid)

            turn = "o"
            display()

        elif turn == "o":
            canvas.create_oval(coord, width="15")
            gridShape[grid[1]][grid[0]] = "o"
            game = gameChecker(grid)

            turn = "x"
            display()

    if 'game' in locals():
        if game == "fin":
            canvas.bind("<Button-1>", init)

#Translates xy coords to  grid coords
def gridCalc(x, y):
    if y in range(30, 170): #Row 1
        gridY = 0
        if x in range(30, 170):
            gridX = 0
        elif x in range(180, 320):
            gridX = 1
        elif x in range(330, 470):
            gridX = 2
        else:
            return("MouseOutOfGrid")

    elif y in range(180, 320): #Row 2
        gridY = 1
        if x in range(30, 170):
            gridX = 0
        elif x in range(180, 320):
            gridX = 1
        elif x in range(330, 470):
            gridX = 2
        else:
            return("MouseOutOfGrid")

    elif y in range(330, 470): #Row 3
        gridY = 2
        if x in range(30, 170):
            gridX = 0
        elif x in range(180, 320):
            gridX = 1
        elif x in range(330, 470):
            gridX = 2
        else:
            return("MouseOutOfGrid")

    else:
        return("MouseOutOfGrid")

    return([gridX, gridY])

#Function to translate grid coords to object coords
def objectLoc(grid):
    #Polygon points
    pointX = [#Points for X
                35+150*grid[0], 35+150*grid[1], #P1
                80+150*grid[0], 100+150*grid[1], #P2
                35+150*grid[0], 165+150*grid[1], #P3
                75+150*grid[0], 165+150*grid[1], #P4
                100+150*grid[0], 130+150*grid[1], #P5
                125+150*grid[0], 165+150*grid[1], #P6
                165+150*grid[0], 165+150*grid[1], #P7
                120+150*grid[0], 100+150*grid[1], #P8
                165+150*grid[0], 35+150*grid[1], #P9
                125+150*grid[0], 35+150*grid[1], #P10
                100+150*grid[0], 70+150*grid[1], #P11
                75+150*grid[0], 35+150*grid[1] #P12
            ]
    #Points for the circle
    pointO = [
                40+150*grid[0], 40+150*grid[1], #P1
                160+150*grid[0], 160+150*grid[1] #P2
            ]

    #returning points
    if turn == "o":
        return(pointO)
    elif turn == "x":
        return(pointX)

def gameChecker(grid):
    x = grid[0]
    y = grid[1]

    # checking basic row win
    if gridShape[y] == ["x", "x", "x"] or gridShape[y] == ["o", "o", "o"]:
        canvas.create_text([250, 250], text="Player {} wins!".format(turn), fill="#ee1fd0",
                           font="CentryGothic 50 bold")
        canvas.create_text([250, 300], text="Please Click to Continue", fill="#ee1fd0", font="centrygothic 20 bold")

        return ("fin")

    # checking for all other types of wins
    else:

        # defining the rows such that all rows are defined in terms of y
        if y == 0:
            y2 = 1
            y3 = 2
        elif y == 1:
            y2 = 0
            y3 = 2
        elif y == 2:
            y2 = 0
            y3 = 1

        # checking to see if all objects in the same position in each row is the same
        if gridShape[y][x] == gridShape[y2][x] == gridShape[y3][x] != "":
            canvas.create_text([250, 250], text="Player {} wins!".format(turn), fill="#ee1fd0",
                               font="CentryGothic 50 bold")
            canvas.create_text([250, 300], text="Please Click to Continue", fill="#ee1fd0",
                               font="centrygothic 20 bold")

            return ("fin")  # returning a value to confirm that the game's outcome has been decided

        elif gridShape[0][0] == gridShape[1][1] == gridShape[2][2] != "":
            canvas.create_text([250, 250], text="Player {} wins!".format(turn), fill="#ee1fd0",
                               font="CentryGothic 50 bold")
            canvas.create_text([250, 300], text="Please Click to Continue", fill="#ee1fd0",
                               font="centrygothic 20 bold")

            return ("fin")

        elif gridShape[0][2] == gridShape[1][1] == gridShape[2][0] != "":
            canvas.create_text([250, 250], text="Player {} wins!".format(turn), fill="#ee1fd0",
                               font="CentryGothic 50 bold")
            canvas.create_text([250, 300], text="Please Click to Continue", fill="#ee1fd0",
                               font="centrygothic 20 bold")

            return ("fin")


        elif "" not in gridShape[0] and "" not in gridShape[1] and "" not in gridShape[2]:
            canvas.create_text([250, 250], text="Tied Game!", fill="#ee1fd0", font="CentryGothic 50 bold")
            canvas.create_text([250, 300], text="Please Click to Continue", fill="#ee1fd0",
                               font="centrygothic 20 bold")

            return ("fin")

        else:
            return (None)  # Do not return anything if none of the conditions are true
main()

