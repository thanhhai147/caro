# Table of Contents
    # Import Library
    # Ai Engine
        # Declaration 0
            # init Variables
            # init Board - 2-dimensional array
            # init board with specific size (10 positions each direction)
        # check whole board
        # check 8 directions of the current move
        # check row
        # check col
        # check first diagnol
        # check second diagnol
        # check Ai win, Human win or not 
        # choose the best Ai move
        # minimax algorithm
        # Print Board in each line
    # Graphic Engine
        # Clear terminal's screen
        # Create Window App
            # Name title of Window App
            # Geometry of Window App
            # Set the Window App a constant size
            # Style 
            # Create Tab control
            # Tab 1 for gameplay
            # Tab 2 for ranking
        # Declaration 1
            # Position of chess we clicked
            # Position of board
            # Coordinate of nodes on chess board
        # Create Canvas
        # Graphic Design
            # Create User click
            # AI move
            # First move of AI
            # Create Graphic Board
        # Declaration 2
            # Define Mouse click on canvas of tkinter
        # Color Chess
        # User's Interface
        # Play game with alternative turns (Ai and Human)

# Contents of Code
# Import library
import math
import copy
from tkinter import Menu
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import *
import tkinter
import turtle
from os import system

# Ai Engine
# init color for user
BackgroundChessBoardColor = "#ffa500"
ColorAiChess = "white"
ColorUserChess = 'black'
# init variables
global realboard # play board
global currentTurn # current turn (AI or Human)
global size # board's size
global positionAi
global positionHuman
global xPosition, yPosition # Position of chess we clicked
global potentialMoves # moves have the highest probability to win
global eightDirects
size = 20 # board - 20x20
graphic_size_board = 25*size+250
history = []
positionAi = {}
positionHuman = {}
potentialMoves = []
eightDirects = [[0, -1], [0, 1], [-1, 0], [1, 0], [-1, -1], [1, 1], [-1, 1], [1, -1]]

# init MouseControl
class MouseControl: # Define Mouse click on canvas of tkinter
    def __init__(self, canvas):
        self.canvas = canvas
        self.canvas.bind('<Double-1>', self.double_click)
    def double_click(self, event):
        for m in range(len(nodes)):
            for n in range(len(nodes)):
                if (nodes[m]-20 < event.x) and (event.x <= nodes[m]+20) and (nodes[n] - 20 <= event.y) and (event.y <= nodes[n]+20):
                    xPosition = nodes[m]
                    yPosition = nodes[n]
                    xBoard = m
                    yBoard = n
                    # print(f'Position on Graphic Board is {xPosition, yPosition} and Position on Real Board {xBoard, yBoard}')
        UserClick(xPosition, yPosition, xBoard, yBoard)

# init nodes
nodes = [] # Coordinate of nodes on chess board
for i in range(size):
    nodes.append(i*(graphic_size_board-100)/size+20)

# init Board - 2-dimensional array
def initBoard():
    board = []
    for i in range(size):
        board.append([None] * size)
    return board

# init board with specific size(10 positions each direction)
realboard = initBoard()

#check whole board
def checkScoreOfBoard(board, parentNode, currentTurn):
    bestScoresList = [checkAllRows(board, parentNode, currentTurn), checkAllCols(board, parentNode, currentTurn), checkAllDiag_1s(board, parentNode, currentTurn), checkAllDiag_2s(board, parentNode, currentTurn)]
    return max(bestScoresList)

# Check scores of all Row directions   
def checkAllRows(board, parentNode, currentTurn):
    score = 0
    consecutive = 0
    openEnds = 0
    for i in range(size):
        for j in range(size):
            currentNode = board[i][j]
            if(currentNode == parentNode):
                consecutive += 1
            elif(currentNode == None and consecutive > 0):
                openEnds += 1
                score += scorePattern(consecutive, openEnds, currentTurn)
                openEnds = 1
                consecutive = 0
            elif(currentNode == None):
                openEnds = 1
            elif(consecutive > 0):
                score += scorePattern(consecutive, openEnds, currentTurn)
                openEnds = 0
                consecutive = 0
            else:
                openEnds = 0
        if(consecutive > 0):
            score += scorePattern(consecutive, openEnds, currentTurn)
            consecutive = 0
            openEnds = 0
    return score

# Check scores of all Column directions
def checkAllCols(board, parentNode, currentTurn):
    score = 0
    consecutive = 0
    openEnds = 0
    for j in range(size):
        for i in range(size):
            currentNode = board[i][j]
            if(currentNode == parentNode):
                consecutive += 1
            elif(currentNode == None and consecutive > 0):
                openEnds += 1
                score += scorePattern(consecutive, openEnds, currentTurn)
                openEnds = 1
                consecutive = 0
            elif(currentNode == None):
                openEnds = 1
            elif(consecutive > 0):
                score += scorePattern(consecutive, openEnds, currentTurn)
                openEnds = 0
                consecutive = 0
            else:
                openEnds = 0
        if(consecutive > 0):
            score += scorePattern(consecutive, openEnds, currentTurn)
            consecutive = 0
            openEnds = 0
    return score

# Checlk scores of all Diagnol_1 directions
def checkAllDiag_1s(board, parentNode, currentTurn):
    score = 0
    consecutive = 0
    openEnds = 0
    for i in range(size):
        for k in range(size):
            if(i + k < size):
                currentNode = board[i + k][0 + k]
                if(currentNode == parentNode):
                    consecutive += 1
                elif(currentNode == None and consecutive > 0):
                    openEnds += 1
                    score += scorePattern(consecutive, openEnds, currentTurn)
                    openEnds = 1
                    consecutive = 0
                elif(currentNode == None):
                    openEnds = 1
                elif(consecutive > 0):
                    score += scorePattern(consecutive, openEnds, currentTurn)
                    openEnds = 0
                    consecutive = 0
                else:
                    openEnds = 0
            else:
                break
        if(consecutive > 0):
            score += scorePattern(consecutive, openEnds, currentTurn)
            consecutive = 0
            openEnds = 0
    for j in range(1, size):
        for k in range(size):
            if(j + k < size):
                currentNode = board[0 + k][j + k]
                if(currentNode == parentNode):
                    consecutive += 1
                elif(currentNode == None and consecutive > 0):
                    openEnds += 1
                    score += scorePattern(consecutive, openEnds, currentTurn)
                    openEnds = 1
                    consecutive = 0
                elif(currentNode == None):
                    openEnds = 1
                elif(consecutive > 0):
                    score += scorePattern(consecutive, openEnds, currentTurn)
                    openEnds = 0
                    consecutive = 0
                else:
                    openEnds = 0
            else:
                break
        if(consecutive > 0):
            score += scorePattern(consecutive, openEnds, currentTurn)
            consecutive = 0
            openEnds = 0
    return score

# Check scores of all Diagnol_2 directions
def checkAllDiag_2s(board, parentNode, currentTurn):
    score = 0
    consecutive = 0
    openEnds = 0
    for i in range(size):
        for k in range(size):
            if(i + k < size):
                currentNode = board[i + k][size - 1 - k]
                if(currentNode == parentNode):
                    consecutive += 1
                elif(currentNode == None and consecutive > 0):
                    openEnds += 1
                    score += scorePattern(consecutive, openEnds, currentTurn)
                    openEnds = 1
                    consecutive = 0
                elif(currentNode == None):
                    openEnds = 1
                elif(consecutive > 0):
                    score += scorePattern(consecutive, openEnds, currentTurn)
                    openEnds = 0
                    consecutive = 0
                else:
                    openEnds = 0
            else:
                break
        if(consecutive > 0):
            score += scorePattern(consecutive, openEnds, currentTurn)
            consecutive = 0
            openEnds = 0
    for j in range(1, size):
        for k in range(size):
            if(size - 1 - j - k):
                currentNode = board[0 + k][size - 1 - j - k]
                if(currentNode == parentNode):
                    consecutive += 1
                elif(currentNode == None and consecutive > 0):
                    openEnds += 1
                    score += scorePattern(consecutive, openEnds, currentTurn)
                    openEnds = 1
                    consecutive = 0
                elif(currentNode == None):
                    openEnds = 1
                elif(consecutive > 0):
                    score += scorePattern(consecutive, openEnds, currentTurn)
                    openEnds = 0
                    consecutive = 0
                else:
                    openEnds = 0
            else:
                break
        if(consecutive > 0):
            score += scorePattern(consecutive, openEnds, currentTurn)
            consecutive = 0
            openEnds = 0
    return score

# Caculate score for the patterns
def scorePattern(consecutive, openEnds, currentTurn):
    if(openEnds == 0):
        return 0
    if(consecutive >= 5):
        return 200000000000
    elif(consecutive == 4):
        if(openEnds == 1):
            if(currentTurn):
                return 100000000
            return 50
        else:
            if(currentTurn):
                return 100000000
            return 500000
    elif(consecutive == 3):
        if(openEnds == 1):
            if(currentTurn):
                return 7
            return 5
        else:
            if(currentTurn):
                return 10000
            return 50
    elif(consecutive == 2):
        if(openEnds == 1):
            return 2
        else:
            return 5
    elif(consecutive == 1):
        if(openEnds == 1):
            return 0.5
        else:
            return 1

# Check Potential moves
def checkPotentialMoves(board, lastPosition):
    subPotentialMoves = []
    for k in range(8):
        i = lastPosition["i"] + eightDirects[k][0]
        j = lastPosition["j"] + eightDirects[k][1] 
        if(i < size and i >= 0 and j < size and j >= 0 and board[i][j] == None):
            subPotentialMoves.append({"i": i, "j": j})
    return subPotentialMoves

# Remove repetitive elements in a list
def removeRepeat(list):
    subList = []
    for item in list:
        if(item not in subList):
            subList.append(item)
    return subList

# check 8 directions of the current move
def checkDirections(board, lastPosition):
    lastMove = board[lastPosition["i"]][lastPosition["j"]]
    check = {}
    # check Row
    check["row"] = checkRow(board, lastMove, lastPosition)
    # check Col
    check["col"] = checkCol(board, lastMove, lastPosition)
    # check diag_1
    check["diag_1"] = checkDiag_1(board, lastMove, lastPosition)
    # check diag_2
    check["diag_2"] = checkDiag_2(board, lastMove, lastPosition)
    return check

# check row
def checkRow(board, lastMove, lastPosition):
    # count number of attack's mates (there are always more one mate)
    countStreak = 1
    # count number of defend's mates
    countAgainst = 0
    # check left direction
    for i in range(1, 5):
        # left move
        if lastPosition["j"] - i >= 0:
            currentMove = board[lastPosition["i"]][lastPosition["j"] - i]
            if currentMove == lastMove:
                # same current
                countStreak += 1
            else:
                if(currentMove == None):
                    break
                else:
                    countAgainst += 1
                    break
        else:
            #out of board's range
            break
    # check right direction
    for i in range(1, 5):
        if lastPosition["j"] + i < size:
            # right move
            currentMove = board[lastPosition["i"]][lastPosition["j"] + i]
            if currentMove == lastMove:
                countStreak += 1
            else:
                if(currentMove == None):
                    break
                else:
                    countAgainst += 1
                    break
        else:
            break
    # return total of attack mates and defend mates
    return {"streak": countStreak, "against": countAgainst}

# check col
def checkCol(board, lastMove, lastPosition):
    countStreak = 1
    countAgainst = 0
    # check above direction
    for i in range(1, 5):
        if lastPosition["i"] - i >= 0:
            # above move
            currentMove = board[lastPosition["i"] - i][lastPosition["j"]]
            if currentMove == lastMove:
                countStreak += 1
            else:
                if(currentMove == None):
                    break
                else:
                    countAgainst += 1
                    break
        else:
            break
    # check below direction
    for i in range(1, 5):
        if lastPosition["i"] + i < size:
            # below move
            currentMove = board[lastPosition["i"] + i][lastPosition["j"]]
            if currentMove == lastMove:
                countStreak += 1
            else:
                if(currentMove == None):
                    break
                else:
                    countAgainst += 1
                    break
        else:
            break
    return {"streak": countStreak, "against": countAgainst}

# check first diagnol
def checkDiag_1(board, lastMove, lastPosition):
    countStreak = 1
    countAgainst = 0
    # check left_above direction
    for i in range(1, 5):
        if lastPosition["i"] - i >= 0 and lastPosition["j"] - i >= 0:
            # left_above move
            currentMove = board[lastPosition["i"] - i][lastPosition["j"] - i]
            if currentMove == lastMove:
                countStreak += 1
            else:
                if(currentMove == None):
                    break
                else:
                    countAgainst += 1
                    break
        else:
            break
    # check right_below direction
    for i in range(1, 5):
        if lastPosition["i"] + i < 10 and lastPosition["j"] + i < size:
            # right_below move
            currentMove = board[lastPosition["i"] + i][lastPosition["j"] + i]
            if currentMove == lastMove:
                countStreak += 1
            else:
                if(currentMove == None):
                    break
                else:
                    countAgainst += 1
                    break
        else:
            break
    return {"streak": countStreak, "against": countAgainst}

# check second diagnol
def checkDiag_2(board, lastMove, lastPosition):
    countStreak = 1
    countAgainst = 0
    # check right_above direction
    for i in range(1, 5):
        if lastPosition["i"] - i >= 0 and lastPosition["j"] + i < size:
            # right_above move
            currentMove = board[lastPosition["i"] - i][lastPosition["j"] + i]
            if currentMove == lastMove:
                countStreak += 1
            else:
                if(currentMove == None):
                    break
                else:
                    countAgainst += 1
                    break
        else:
            break
    # check left_below direction
    for i in range(1, 5):
        if lastPosition["i"] + i < 10 and lastPosition["j"] - i >= 0:
            # left_below move
            currentMove = board[lastPosition["i"] + i][lastPosition["j"] - i]
            if currentMove == lastMove:
                countStreak += 1
            else:
                if(currentMove == None):
                    break
                else:
                    countAgainst += 1
                    break
        else:
            break
    return {"streak": countStreak, "against": countAgainst}

#check Ai win, Human win or not 
def checkWin(board, lastPositionAi, lastPositionHuman):
    directionAi = checkDirections(board, lastPositionAi)
    directionHuman = checkDirections(board, lastPositionHuman)
    for direction in directionAi.values():
        if direction["streak"] == 5 and direction["against"] < 2:
            return "Ai win"
    for direction in directionHuman.values():
        if direction["streak"] == 5 and direction["against"] < 2:
            return "Human win"
    return None

#choose the best Ai move
def chooseMove(board, subPotentialMoves):
    bestScore = -math.inf
    bestMove = {}
    alpha = -math.inf
    beta = math.inf
    # Loop through all potential moves
    for move in subPotentialMoves:
        board[move["i"]][move["j"]] = "o"
        # Find the next potential moves
        subList = copy.deepcopy(subPotentialMoves)
        subList.remove(move)
        subList.extend(checkPotentialMoves(board, move))
        subList = removeRepeat(subList)
        subList.reverse()
        # score the board with the depth is 1
        score = minimax(board, subList, move, positionHuman, 2, alpha, beta, False)
        board[move["i"]][move["j"]] = None
        if(score > bestScore):
            bestScore = score
            bestMove = move
        # alpha-beta prunning
        alpha = max(score, alpha)
        if(beta <= alpha):
            break
    return bestMove

#minimax algorithm  
def minimax(board, subPotentialMoves, lastPositionAi, lastPositionHuman, depth, alpha, beta ,maximizing):
    # Check result of the board
    result = checkWin(board, lastPositionAi, lastPositionHuman)
    # Return the score of the board when one side wins or out of tree's depth
    if result == "Ai win" or result == "Human win" or depth == 0:
        if(maximizing):
            currentTurn = True
        else:                              
            currentTurn = False
        # Check score of Ai's moves
        aiScore = checkScoreOfBoard(board, "o", currentTurn)
        # Check score of Human's moves
        humanScore = checkScoreOfBoard(board, "x", not currentTurn)
        return aiScore - humanScore
    else:
        if(maximizing):
            # Choose the best move with the highest score
            bestScore = -math.inf
            # Loop through all potential moves
            for move in subPotentialMoves:
                board[move["i"]][move["j"]] = "o"
                subList = copy.deepcopy(subPotentialMoves)
                subList.remove(move)
                subList.extend(checkPotentialMoves(board, move))
                subList = removeRepeat(subList)
                subList.reverse()
                # Score the board with depth - 1
                score = minimax(board, subList, move, lastPositionHuman, depth - 1, alpha, beta ,not maximizing)
                board[move["i"]][move["j"]] = None
                # Choose the best Score
                bestScore = max(score, bestScore)
                # alpha-beta prunning
                alpha = max(score, alpha)
                if(beta <= alpha):
                    break
            return bestScore
        else:
            # Choose the best move with the lowest score
            bestScore = math.inf
            # Loop through all potential moves
            for move in subPotentialMoves:
                board[move["i"]][move["j"]] = "x"
                subList = copy.deepcopy(subPotentialMoves)
                subList.remove(move)
                subList.extend(checkPotentialMoves(board, move))
                subList = removeRepeat(subList)
                subList.reverse()
                # Score the board with the depth - 1
                score = minimax(board, subList, lastPositionAi, move, depth - 1, alpha, beta ,not maximizing)
                board[move["i"]][move["j"]] = None
                # Choose the best Score
                bestScore = min(score, bestScore)
                # Alpha-beta prunning
                beta = min(score, beta)
                if(beta <= alpha):
                    break
            return bestScore

# Print Board in each line
def printBoard(board):
    for i in range(10):
        print(board[i])

# Graphic Engine
# Clear terminal's screen
def clear(): 
    _ = system('clear') 
clear()

# Create Window App
window = tkinter.Tk()
window.title("GOMOKU") # Name title of Window App
window.geometry(str(graphic_size_board)+"x"+str(graphic_size_board)) # Geometry of Window App
window.resizable(width=0, height=0) # Set the Window App a constant size

# Style 
style = ttk.Style()

style.theme_create("maintheme", settings={
    "TFrame": {
        "configure": {
            "background": BackgroundChessBoardColor
        }
    }
})

style.theme_use("maintheme")

tab_control = ttk.Notebook(window) # Create Tab control

tab_1_gameplay = ttk.Frame(tab_control) # Tab 1 for Gameplay
tab_control.add(tab_1_gameplay, text="Gameplay")

# tab_2_ranking = ttk.Frame(tab_control) # Tab 2 for Ranking
# tab_control.add(tab_2_ranking, text="Ranking")

# Create Canvas
canvas = tkinter.Canvas(tab_1_gameplay, width=graphic_size_board-100, height=graphic_size_board-100)
canvas.grid(padx=5, pady=5, row=5, column=0, rowspan=10, columnspan=10)
canvas.place(relx=0.5, rely=0.55, anchor="center")
s1 = turtle.TurtleScreen(canvas)
s1.bgcolor(BackgroundChessBoardColor)
draw = turtle.RawTurtle(s1) # To draw colums and rows

# Graphic Design
def UserClick(xPosition,yPosition, xBoard, yBoard):
    global realboard
    global positionAi
    global positionHuman
    global potentialMoves
    if realboard[xBoard][yBoard] == None:
        # User's turn ("b" is for "black")
        positionHuman["i"] = xBoard
        positionHuman["j"] = yBoard
        if(positionHuman in potentialMoves):
            potentialMoves.remove(positionHuman)
        potentialMoves.extend(checkPotentialMoves(realboard, positionHuman))
        potentialMoves = removeRepeat(potentialMoves)
        draw_stone(xPosition-200,190-yPosition,colors["b"])
        board[xBoard][yBoard]="b"
        realboard[xBoard][yBoard] = "x"
        result = checkWin(realboard, positionAi, positionHuman)
        if(result == "Ai win" or result == "Human win"):
            messagebox.showinfo("RESULT",result)
        else:
            # Ai's turn
            result = AiPlay()
            if(result == "Ai win" or result == "Human win"):
                messagebox.showinfo("RESULT",result)

def AiMove(xBoard, yBoard):
    draw_stone(nodes[xBoard]-200, 190-nodes[yBoard], colors["w"])
    board[xBoard][yBoard] = "w"
    history.append(positionAi)
    if len(history)>=2:
        non_outline_stone(nodes[history[len(history) - 2]["i"]]-200, 190-nodes[history[len(history) - 2]["j"]], colors["w"])
    outline_stone(nodes[xBoard]-200, 190-nodes[yBoard], colors["w"])

def firtstMoveAi():
    global realboard
    global positionAi
    if (size % 2 == 0):
        positionAi["i"] = size//2 - 1
        positionAi["j"] = size//2 - 1
        realboard[size//2 - 1][size//2 - 1] = "o"
        potentialMoves.extend(checkPotentialMoves(realboard, positionAi))
        AiMove(size//2 - 1,size//2 - 1)
    else:
        positionAi["i"] = size//2
        positionAi["j"] = size//2
        realboard[size//2][size//2] = "o"
        potentialMoves.extend(checkPotentialMoves(realboard, positionAi))
        AiMove(size//2,size//2)

def Graphic_Board(size):
    # Create Board
    global board 
    board = []
    for i in range(size):
        board.append([" "]*size)
    side = size/2
    draw.speed(0.5)
    draw.penup()
    # Create Columns
    i=-1
    for start in range(size):
        draw.goto((graphic_size_board-100)/size*start-(graphic_size_board-100)/2, (graphic_size_board-100)/size*(side+side*i)-(graphic_size_board-100)/2)
        draw.pendown()
        i *= -1
        draw.goto((graphic_size_board-100)/size*start-(graphic_size_board-100)/2, (graphic_size_board-100)/size*(side+side*i)-(graphic_size_board-100)/2)  
        draw.penup()
    # Create Rows
    i=1
    for start in range(size):
        draw.goto((graphic_size_board-100)/size*(side+side*i)-(graphic_size_board-100)/2, (graphic_size_board-100)/size*start-(graphic_size_board-100)/2)
        draw.pendown()
        i *= -1
        draw.goto((graphic_size_board-100)/size*(side+side*i)-(graphic_size_board-100)/2, (graphic_size_board-100)/size*start-(graphic_size_board-100)/2)
        draw.penup()
    draw.ht() # Hide Cursor
    # Create Mouse Click
    MouseControl(canvas) 
    for key in colors:
        colors[key].ht()
        colors[key].penup()
        colors[key].speed(0)

# Color Chess
colors = {"w":turtle.RawTurtle(canvas),"b":turtle.RawTurtle(canvas)}
colors["w"].color(ColorAiChess)
colors["b"].color(ColorUserChess)
# Outline the last Ai chess
def outline_stone(x, y, colturtle):
    colturtle.goto(x-4.5*(graphic_size_board-100)/size+1.5,y+4.5*(graphic_size_board-100)/size+8.5)
    colturtle.speed(0)
    for i in range(4):
        colturtle.pen(pencolor="red", pensize=1.5)
        colturtle.pendown()
        colturtle.begin_fill()
        colturtle.forward((graphic_size_board-100)/size)
        colturtle.right(90)
        colturtle.end_fill()
        colturtle.penup()
# Erase outline of the previous Ai Chess before the last chess
def non_outline_stone(x, y, colturtle):
    colturtle.goto(x-4.5*(graphic_size_board-100)/size+1.5,y+4.5*(graphic_size_board-100)/size+8.5)
    colturtle.speed(0)
    for i in range(4):
        colturtle.pen(pencolor=BackgroundChessBoardColor, pensize=1.5)
        colturtle.pendown()
        colturtle.begin_fill()
        colturtle.forward((graphic_size_board-100)/size)
        colturtle.right(90)
        colturtle.end_fill()
    for i in range(4):
        colturtle.pen(pencolor="black", pensize=1)
        colturtle.pendown()
        colturtle.begin_fill()
        colturtle.forward((graphic_size_board-100)/size)
        colturtle.right(90)
        colturtle.end_fill()
        colturtle.penup()
# Draw an Ai or User chess
def draw_stone(x,y,colturtle):
    colturtle.pen(pencolor=BackgroundChessBoardColor)
    # colturtle.goto(x,y-(graphic_size_board-100)/size/2*25/100) # This is for board 10x10
    colturtle.goto(x-4*(graphic_size_board-100)/size+2,y+4*(graphic_size_board-100)/size-(graphic_size_board-100)/size/2*25/100) # This is for board 20x20
    colturtle.pendown()
    colturtle.begin_fill()
    colturtle.circle((graphic_size_board-100)/size/2*75/100)
    colturtle.end_fill()
    colturtle.penup()

# User's Interface
def initialize():
    # Title
    Title = tkinter.Label(tab_1_gameplay, bg=BackgroundChessBoardColor, text="GOMOKU", font=("Times New Roman", 35, "bold"))
    Title.grid(row=0, column=0,columnspan=10)
    Title.place(relx = 0.5, rely = 0.05, anchor = "center")

    # Running file !!!
    print(f' - Nodes is {nodes}')
    Graphic_Board(size)
    tab_control.pack(expand=1, fill='both')
    firtstMoveAi()
    window.mainloop()

# Play game with alternative turns (Ai and Human)
def AiPlay():
    global realboard
    global positionAi
    global positionHuman
    global potentialMoves
    result = checkWin(realboard, positionAi, positionHuman)
    # printBoard(realboard)
    if (result == "Ai win" or result == "Human win"):
        print(result)
    else:
        # choose the best move
        positionAi = chooseMove(realboard, potentialMoves)
        # print(f' - Ai Position is {positionAi}')
        potentialMoves.remove(positionAi)
        potentialMoves.extend(checkPotentialMoves(realboard, positionAi))
        potentialMoves = removeRepeat(potentialMoves)
        # play with the best move
        realboard[positionAi["i"]][positionAi["j"]] = "o"
        AiMove(positionAi["i"], positionAi["j"])
        # check result
        result = checkWin(realboard, positionAi, positionHuman)
    return result

if __name__ == "__main__":
    initialize()
