import numpy as np

from position_eval import check8Directions

def eval_board(board, node, subPotentialMoves):
    # ai_must_win = set()
    # human_must_win = set()
    val = 0
    # att = 0
    # deft = 0
    for position in subPotentialMoves:
        board[position[0]][position[1]] = node
        v = eval_pos(board, position, node)
        board[position[0]][position[1]] = 0
        if v > 100: val = val + v if node > 0 else val - v
        # if(v > scoreTable(5, 0, 1)): ai_must_win.add(position) if node > 0 else human_must_win.add(position)
    # if(len(ai_must_win) >= 2): att += np.inf
    # if(len(human_must_win) >= 2): deft -= np.inf
    return val   
            
def eval_pos(board, position, node):
    positionCheck = check8Directions(board, position)
    return sum([scoreTable(direction["streak"], direction["blocked"], node) for direction in positionCheck])

def scoreTable(streak, blocked, node):
    if(blocked >= 2): return 0
    if(streak >= 5): return 10000000
    if(streak == 4 and blocked == 0): return 100000
    if(streak == 4 and blocked == 1): return 100000
    if(streak == 3 and blocked == 0): return 10000
    if(streak == 3 and blocked == 1): return 100
    if(streak == 2 and blocked == 0): return 100
    if(streak == 2 and blocked == 1): return 10
    if(streak == 1 and blocked == 0): return 10
    if(streak == 1 and blocked == 1): return 1
    
