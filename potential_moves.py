import copy
eightDirects = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, 1), (-1, 1), (1, -1))

# Check Potential moves
def checkPotentialMoves(board, lastPosition):
    subPotentialMoves = set()
    for k in range(8):
        i = lastPosition[0] + eightDirects[k][0]
        j = lastPosition[1] + eightDirects[k][1] 
        if(i < board.shape[0] and i >= 0 and j < board.shape[1] and j >= 0 and board[i][j] == 0): subPotentialMoves.add((i, j))
    return subPotentialMoves

def expandPotentialMoves(board, potentialMoves, lastPosition):
    subPotentialMoves = set(copy.deepcopy(potentialMoves))
    subPotentialMoves.discard(lastPosition)
    subPotentialMoves.update(checkPotentialMoves(board, lastPosition))
    listSub = list(subPotentialMoves)
    listSub.reverse()
    return listSub