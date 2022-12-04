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
import copy
from msilib.schema import Directory
from tkinter import Menu
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import *
import tkinter
import turtle
from os import system
from board_eval import eval_board
from potential_moves import expandPotentialMoves
from position_eval import checkWin

# Ai Engine
# init color for user
BackgroundChessBoardColor = "#ffa500"
ColorAiChess = "white"
ColorUserChess = "black"
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
potentialMoves = []
eightDirects = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, 1), (-1, 1), (1, -1))
treeDepth = 2  

# zebris hashing
rng = np.random.default_rng()
M_Ai = rng.integers(low=100**5, high=100**9, size=(size, size))
M_Human = rng.integers(low=100**5, high=100**9, size=(size, size))
board_hash = 0
eval_dict = {}

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

#choose the best Ai move
def chooseMove(board, subPotentialMoves, current_board_hash):
    global threads
    global treeDepth
    global positionHuman
    global M_Ai
    bestScore = -np.inf
    bestMove = {}
    alpha = -np.inf
    beta = np.inf
    # Loop through all potential moves
    for move in subPotentialMoves:
        board[move[0]][move[1]] = 1
        # Find the next potential moves
        expanded = expandPotentialMoves(board, subPotentialMoves, move)
        # temp board hash
        temp_board_hash = current_board_hash ^ M_Ai[move[0]][move[1]]
        # score the board with the depth is 1
        score = minimax(board, expanded, move, positionHuman, treeDepth - 1, alpha, beta, False, temp_board_hash)
        board[move[0]][move[1]] = 0
        if(score > bestScore):
            bestScore = score
            bestMove = move
        # alpha-beta prunning
        alpha = max(score, alpha)
        if(beta <= alpha): break
    return bestMove

#minimax algorithm  
def minimax(board, subPotentialMoves, lastPositionAi, lastPositionHuman, depth, alpha, beta, maximizing, current_board_hash):
    global M_Ai
    global M_Human
    # Check result of the board
    result = checkWin(board, lastPositionAi, lastPositionHuman)
    # Return the score of the board when one side wins or out of tree's depth
    if result == "Ai win" or result == "Human win" or depth == 0:
        key_board_hash = str(current_board_hash) 
        if(key_board_hash in eval_dict.keys()): return eval_dict[key_board_hash]
        current_eval = eval_board(board, 1, subPotentialMoves) + eval_board(board, -1, subPotentialMoves)
        eval_dict[key_board_hash] = current_eval
        return current_eval
    
    if(maximizing):
        # Choose the best move with the highest score
        bestScore = -np.inf
        # Loop through all potential moves
        for move in subPotentialMoves:
            board[move[0]][move[1]] = 1
            # expand potential moves
            expanded = expandPotentialMoves(board, subPotentialMoves, move)
            # update temp board hash
            temp_board_hash = current_board_hash ^ M_Ai[move[0]][move[1]]
            # Score the board with depth - 1
            score = minimax(board, expanded, move, lastPositionHuman, depth - 1, alpha, beta , False, temp_board_hash)
            board[move[0]][move[1]] = 0
            # Choose the best Score
            bestScore = max(score, bestScore)
            # alpha-beta prunning
            alpha = max(score, alpha)
            if(beta <= alpha): break
        return bestScore
    else:
        # Choose the best move with the lowest score
        bestScore = np.inf
        # Loop through all potential moves
        for move in subPotentialMoves:
            board[move[0]][move[1]] = -1
            # expand potential moves
            expanded = expandPotentialMoves(board, subPotentialMoves, move)
            # update temp board hash
            temp_board_hash = current_board_hash ^ M_Human[move[0]][move[1]]
            # Score the board with the depth - 1
            score = minimax(board, expanded, lastPositionAi, move, depth - 1, alpha, beta , True, temp_board_hash)
            board[move[0]][move[1]] = 0
            # Choose the best Score
            bestScore = min(score, bestScore)
            # Alpha-beta prunning
            beta = min(score, beta)
            if(beta <= alpha):
                break
        return bestScore

# Graphic Engine
# Clear terminal's screen
def clear(): 
    _ = system('cls') 
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
    global board_hash
    global M_Human
    if realboard[xBoard][yBoard] == 0:
        # User's turn ("b" is for "black")
        positionHuman = (xBoard, yBoard)
        # expand potential moves
        potentialMoves = expandPotentialMoves(realboard, potentialMoves, positionHuman)
        # update board hash
        board_hash ^= M_Human[xBoard][yBoard]  
        # draw stone
        draw_stone(xPosition-200,190-yPosition,colors["b"])
        board[xBoard][yBoard]="b"
        realboard[xBoard][yBoard] = -1
        # check win 
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
    global potentialMoves
    global board_hash
    global M_Ai
    if (size % 2 == 0):
        positionAi = (size//2 - 1, size//2 - 1)
        realboard[size//2 - 1][size//2 - 1] = 1
        AiMove(size//2 - 1,size//2 - 1)
    else:
        positionAi = (size//2, size//2)
        realboard[size//2][size//2] = 1
        AiMove(size//2,size//2)
    # expand potential moves
    potentialMoves = expandPotentialMoves(realboard, potentialMoves, positionAi)
    # update board hash
    board_hash ^= M_Ai[positionAi[0]][positionAi[1]]

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
    global board_hash
    global M_Ai
    result = checkWin(realboard, positionAi, positionHuman)
    if (result == "Ai win" or result == "Human win"):
        print(result)
    else:
        # choose the best move
        positionAi = chooseMove(realboard, potentialMoves, board_hash)
        # play with the best move
        realboard[positionAi[0]][positionAi[1]] = 1
        # expand potential moves
        potentialMoves = expandPotentialMoves(realboard, potentialMoves, positionAi)
        # update board hash
        board_hash ^= M_Ai[positionAi[0]][positionAi[1]]
        # draw stone
        AiMove(positionAi[0], positionAi[1])
        # check result
        result = checkWin(realboard, positionAi, positionHuman)
    return result

if __name__ == "__main__":
    initialize()
