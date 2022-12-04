# check 8 directions at the same time
from turtle import pos


def check8Directions(board, lastPosition):
    lastMove = board[lastPosition[0]][lastPosition[1]]
    check = [{"streak": 1, "blocked": 0, "leftStop": False, "rightStop": False}, {"streak": 1, "blocked": 0, "leftStop": False, "rightStop": False}, {"streak": 1, "blocked": 0, "leftStop": False, "rightStop": False}, {"streak": 1, "blocked": 0, "leftStop": False, "rightStop": False}]
    for i in range(-1, 2, 2):
        for j in range(1, 6):
            # row direction
            position = [[lastPosition[0], lastPosition[1]+i*j], [lastPosition[0] + i*j,lastPosition[1]], [lastPosition[0] + i*j, lastPosition[1] + i*j], [lastPosition[0] + i*j, lastPosition[1] + (-i*j)]]
            if ((position[0][1] >= 0) and (position[0][1] < board.shape[0]) and (not check[0]["rightStop"] if i == 1 else not check[0]["leftStop"])): checkCurrentMove(lastMove, board[position[0][0]][position[0][1]], i, check[0])
            # column direction
            if ((position[1][0] >= 0) and (position[1][0] < board.shape[0]) and (not check[1]["rightStop"] if i == 1 else not check[1]["leftStop"])): checkCurrentMove(lastMove, board[position[1][0]][position[1][1]], i, check[1])
            # diag_1 direction
            if ((position[2][0] >= 0) and (position[2][1] >= 0) and (position[2][0] < board.shape[0]) and (position[2][1] < board.shape[0]) and (not check[2]["rightStop"] if i == 1 else not check[2]["leftStop"])): checkCurrentMove(lastMove, board[position[2][0]][position[2][1]], i, check[2])
            # diag_2 direction
            if ((position[3][0] < board.shape[0]) and (position[3][1] < board.shape[0]) and (position[3][0] >= 0) and (position[3][1] >= 0) and (not check[3]["rightStop"] if i == 1 else not check[3]["leftStop"])): checkCurrentMove(lastMove, board[position[3][0]][position[3][1]], i, check[3])
    return check

def checkCurrentMove(lastMove, currentMove, direction, check):
    if(currentMove == lastMove): check["streak"] += 1 
    elif(currentMove != 0): 
        check["blocked"] += 1
        if(direction == 1): check["rightStop"] = True 
        else: check["leftStop"] = True
    else:
        if(direction == 1): check["rightStop"] = True 
        else: check["leftStop"] = True

#check Ai win, Human win or not 
def checkWin(board, lastPositionAi, lastPositionHuman):
    for aiDirection, humanDirection in zip(check8Directions(board, lastPositionAi), check8Directions(board, lastPositionHuman)):
        if aiDirection["streak"] >= 5 and aiDirection["blocked"] < 2:
            return "Ai win"
        elif humanDirection["streak"] >= 5 and humanDirection["blocked"] < 2:
            return "Human win"
    return None