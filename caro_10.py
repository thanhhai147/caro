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
from inspect import currentframe
import numpy as np
import math
import copy
from msilib.schema import Directory
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
positionAi = ()
positionHuman = ()
potentialMoves = set()
eightDirects = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, 1), (-1, 1), (1, -1))
treeDepth = 2

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
nodes = [i*(graphic_size_board-100)/size+20 for i in range(size)] # Coordinate of nodes on chess board

# init board with specific size
realboard = np.zeros([size, size])

#check whole board
def checkScoreOfBoard(board, parentNode, currentTurn, subPotentialMoves):
    iMin = math.inf
    iMax = -math.inf
    jMin = math.inf
    jMax = -math.inf
    for i, j in subPotentialMoves:
        iMin = min(iMin, i)
        iMax = max(iMax, j)
        jMin = min(jMin, j)
        jMax = max(jMax, j)
    subBoard = board[iMin:iMax+1,jMin:jMax+1]
    return checkScore8Directions(subBoard, parentNode, currentTurn)

def checkScore8Directions(board, parentNode, currentTurn):
    score_check = [{"score": 0, "consecutive": 0, "openEnds": 0}, {"score": 0, "consecutive": 0, "openEnds": 0}, {"score": 0, "consecutive": 0, "openEnds": 0}, {"score": 0, "consecutive": 0, "openEnds": 0}]
    i_length = board.shape[0]
    j_length = board.shape[1]
    for k in range(i_length if i_length > j_length else j_length):
        # check rows
        if k < i_length: checkScoreOneDirection(parentNode, board[k,:], currentTurn, score_check[0])
        # check columns
        if k < j_length: checkScoreOneDirection(parentNode, board[:,k], currentTurn, score_check[1])
        # check diag_1s
        if k < j_length: checkScoreOneDirection(parentNode, np.diag(board, k), currentTurn, score_check[2])
        if k+1 < i_length: checkScoreOneDirection(parentNode, np.diag(board, -k-1), currentTurn, score_check[2])
        # check diag_2s
        if k < j_length: checkScoreOneDirection(parentNode, np.diag(np.fliplr(board), k), currentTurn, score_check[3])
        if k+1 < i_length: checkScoreOneDirection(parentNode, np.diag(np.fliplr(board), -k-1), currentTurn, score_check[3])
    return sum([direction["score"] for direction in score_check])

def checkScoreOneDirection(parentNode, currentDirection, currentTurn, score_check):
    for currentNode in currentDirection:
        if(currentNode == parentNode):
            score_check["consecutive"] += 1
        elif(currentNode == 0 and score_check["consecutive"] > 0):
            score_check["openEnds"] += 1
            score_check["score"] += scorePattern(score_check["consecutive"], score_check["openEnds"], currentTurn)
            score_check["openEnds"] = 1
            score_check["consecutive"] = 0
        elif(currentNode == 0):
            score_check["openEnds"] = 1
        elif(score_check["consecutive"] > 0):
            score_check["score"] += scorePattern(score_check["consecutive"], score_check["openEnds"], currentTurn)
            score_check["openEnds"] = 0
            score_check["consecutive"] = 0
        else:
            score_check["openEnds"] = 0
    if(score_check["consecutive"] > 0): score_check["score"] += scorePattern(score_check["consecutive"], score_check["openEnds"], currentTurn)
    score_check["consecutive"] = 0
    score_check["openEnds"] = 0

# Caculate score for the patterns
def scorePattern(consecutive, openEnds, currentTurn):
    if(openEnds == 0):
        return 0
    if(consecutive >= 5):
        return 900000000000
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
    subPotentialMoves = set()
    for k in range(8):
        i = lastPosition[0] + eightDirects[k][0]
        j = lastPosition[1] + eightDirects[k][1] 
        if(i < size and i >= 0 and j < size and j >= 0 and board[i][j] == 0): subPotentialMoves.add((i, j))
    return subPotentialMoves

# check 8 directions at the same time
def check8Directions(board, lastPosition):
    lastMove = board[lastPosition[0]][lastPosition[1]]
    check = [{"streak": 1, "against": 0, "leftStop": False, "rightStop": False}, {"streak": 1, "against": 0, "leftStop": False, "rightStop": False}, {"streak": 1, "against": 0, "leftStop": False, "rightStop": False}, {"streak": 1, "against": 0, "leftStop": False, "rightStop": False}]
    for i in range(-1, 2, 2):
        for j in range(1, 5):
            # row direction
            if (lastPosition[1] + i*j >= 0 and lastPosition[1] + i*j < size and not check[0]["rightStop"] if i == 1 else not check[0]["leftStop"]): checkCurrentMove(lastMove, board[lastPosition[0]][lastPosition[1] + i*j], i, check[0])
            # column direction
            if (lastPosition[0] + i*j >= 0 and lastPosition[0] + i*j < size and not check[1]["rightStop"] if i == 1 else not check[1]["leftStop"]): checkCurrentMove(lastMove, board[lastPosition[0] + i*j][lastPosition[1]], i, check[1])
            # diag_1 direction
            if (lastPosition[0] + i*j >= 0 and lastPosition[1] + i*j >= 0 and lastPosition[0] + i*j < size and lastPosition[1] + i*j < size and not check[2]["rightStop"] if i == 1 else not check[2]["leftStop"]): checkCurrentMove(lastMove, board[lastPosition[0] + i*j][lastPosition[1] + i*j], i, check[2])
            # diag_2 direction
            if (lastPosition[0] + i*j >= 0 and lastPosition[0] + i*j < size and lastPosition[1] + (-i*j) >= 0 and lastPosition[1] + (-i*j) < size and not check[3]["rightStop"] if i == 1 else not check[3]["leftStop"]): checkCurrentMove(lastMove, board[lastPosition[0] + i*j][lastPosition[1] + (-i*j)], i, check[3])
    return check

def checkCurrentMove(lastMove, currentMove, direction, check):
    if(currentMove == lastMove): check["streak"] += 1 
    elif(currentMove != 0): 
        check["against"] += 1
        if(direction == 1): check["rightStop"] = True 
        else: check["leftStop"] = True
    else:
        if(direction == 1): check["rightStop"] = True 
        else: check["leftStop"] = True

#check Ai win, Human win or not 
def checkWin(board, lastPositionAi, lastPositionHuman):
    for aiDirection, humanDirection in zip(check8Directions(board, lastPositionAi), check8Directions(board, lastPositionHuman)):
        if aiDirection["streak"] >= 5 and aiDirection["against"] < 2:
            return "Ai win"
        elif humanDirection["streak"] >= 5 and humanDirection["against"] < 2:
            return "Human win"
    return None

#choose the best Ai move
def chooseMove(board, subPotentialMoves):
    global threads
    global treeDepth
    global positionHuman
    bestScore = -math.inf
    bestMove = {}
    alpha = -math.inf
    beta = math.inf
    # executor = ThreadPoolExecutor(max_workers=threads)
    # Loop through all potential moves
    for move in subPotentialMoves:
        board[move[0]][move[1]] = 1
        # Find the next potential moves
        subSet = copy.deepcopy(subPotentialMoves)
        subSet.discard(move)
        subSet.update(checkPotentialMoves(board, move))
        # score the board with the depth is 1
        score = minimax(board, subSet, move, positionHuman, treeDepth, alpha, beta, False)
        board[move[0]][move[1]] = 0
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
    if result == "Ai win" or result == "Human win" or depth == 0: return checkScoreOfBoard(board, 1, maximizing, subPotentialMoves) - checkScoreOfBoard(board, -1, not maximizing, subPotentialMoves)
    elif(maximizing):
        # Choose the best move with the highest score
        bestScore = -math.inf
        # Loop through all potential moves
        for move in subPotentialMoves:
            board[move[0]][move[1]] = 1
            subList = copy.deepcopy(subPotentialMoves)
            subList.remove(move)
            subList.update(checkPotentialMoves(board, move))
            # Score the board with depth - 1
            score = minimax(board, subList, move, lastPositionHuman, depth - 1, alpha, beta ,not maximizing)
            board[move[0]][move[1]] = 0
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
            board[move[0]][move[1]] = -1
            subList = copy.deepcopy(subPotentialMoves)
            subList.remove(move)
            subList.update(checkPotentialMoves(board, move))
            # Score the board with the depth - 1
            score = minimax(board, subList, lastPositionAi, move, depth - 1, alpha, beta ,not maximizing)
            board[move[0]][move[1]] = 0
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
    if realboard[xBoard][yBoard] == 0:
        # User's turn ("b" is for "black")
        positionHuman = (xBoard, yBoard)
        if(positionHuman in potentialMoves):
            potentialMoves.remove(positionHuman)
        potentialMoves.update(checkPotentialMoves(realboard, positionHuman))
        draw_stone(xPosition-200,190-yPosition,colors["b"])
        board[xBoard][yBoard]="b"
        realboard[xBoard][yBoard] = -1
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
        non_outline_stone(nodes[history[len(history) - 2][0]]-200, 190-nodes[history[len(history) - 2][1]], colors["w"])
    outline_stone(nodes[xBoard]-200, 190-nodes[yBoard], colors["w"])

def firtstMoveAi():
    global realboard
    global positionAi
    if (size % 2 == 0):
        positionAi = (size//2 - 1, size//2 - 1)
        realboard[size//2 - 1][size//2 - 1] = 1
        potentialMoves.update(checkPotentialMoves(realboard, positionAi))
        AiMove(size//2 - 1,size//2 - 1)
    else:
        positionAi = (size//2, size//2)
        realboard[size//2][size//2] = 1
        potentialMoves.update(checkPotentialMoves(realboard, positionAi))
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
    if (result == "Ai win" or result == "Human win"):
        print(result)
    else:
        # choose the best move
        positionAi = chooseMove(realboard, potentialMoves)
        # print(f' - Ai Position is {positionAi}')
        potentialMoves.remove(positionAi)
        potentialMoves.update(checkPotentialMoves(realboard, positionAi))
        # play with the best move
        realboard[positionAi[0]][positionAi[1]] = 1
        AiMove(positionAi[0], positionAi[1])
        # check result
        result = checkWin(realboard, positionAi, positionHuman)
    return result

if __name__ == "__main__":
    initialize()
