"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    numXs = 0
    numOs = 0
    numEmpty = 0

    if terminal(board):
        return "FINISHED GAME"

    for row in board:
        for cell in row:
            if cell is EMPTY:
                numEmpty += 1
            elif cell is X:
                numXs += 1
            elif cell is O:
                numOs += 1

    if numEmpty == 9 or numXs == numOs:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    listOfActions = set()

    if terminal(board):
        return "GAME FINISHED"

    for row in range(3):
        for cell in range(3):
            if board[row][cell] == EMPTY:
                listOfActions.add((row, cell))

    return listOfActions            


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    newBoardState = copy.deepcopy(board)
    playerTurn = player(newBoardState)

    if action not in actions(board):
        raise Exception

    if playerTurn is X:
        newBoardState[action[0]][action[1]] = X
    elif playerTurn is O:
        newBoardState[action[0]][action[1]] = O
    
    return newBoardState
    


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # If all spots are not filled, check for 3 in a row.
    # Check Vertical; Check Horizontal; Check Diagonal

    #Checking for 3 in a row Vertically
    numXs = 0
    numOs = 0

    for index in range(3):
        for row in board:
            if row[index] == X:
                numXs += 1
            elif row[index] == O:
                numOs += 1
        if numXs == 3:
            return X
        elif numOs == 3:
            return O
        numXs = 0
        numOs = 0
    
    #Checking for 3 in a row Horizontally
    numOs = 0
    numXs = 0

    for row in board:
        for index in range(3):
            if row[index] == X:
                numXs += 1
            elif row[index] == O:
                numOs += 1
        if numXs == 3:
            return X
        elif numOs == 3:
            return O
        numXs = 0
        numOs = 0

    #Lastly, we check for 3 in a row diagonally. First TL -> BR, and then TR -> BL
    numOs = 0
    numXs = 0
    index = 0

    for i in range(3):
        if board[i][index] == X:
            numXs += 1
        elif board[i][index] == O:
            numOs += 1
        index += 1

    if numXs == 3:
        return X
    elif numOs == 3:
        return O

    numOs = 0
    numXs = 0
    index = 2

    for i in range(3):
        if board[i][index] == X:
            numXs += 1
        elif board[i][index] == O:
            numOs += 1
        index -= 1
    
    if numXs == 3:
            return X
    elif numOs == 3:
            return O
    
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    #If all spots are filled, the game is over
    numEmpty = 0
    for row in board:
        for cell in row:
            if cell == EMPTY:
                numEmpty += 1
    
    if winner(board) is not None or numEmpty == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    resultOfWinner = winner(board)

    if resultOfWinner == None:
        return 0
    elif resultOfWinner is X:
        return 1
    elif resultOfWinner is O:
        return -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return NONE

    optimalAction = "This is the action that will give us the optimalValue"
    playerTurn = player(board)

    if playerTurn == X:
        maxValue = -math.inf
        for action in actions(board):
            optimalValue = getMinValue(result(board, action))
            if optimalValue > maxValue:
                maxValue = optimalValue
                optimalAction = action
    elif playerTurn == O:
        minValue = math.inf
        for action in actions(board):
            optimalValue = getMaxValue(result(board, action))
            if optimalValue < minValue:
                minValue = optimalValue
                optimalAction = action
    
    return optimalAction


def getMaxValue(board):
    if terminal(board):
        return utility(board)
    else:
        value = -math.inf
        for action in actions(board):
            resultOfMinValue = getMinValue(result(board, action))
            if resultOfMinValue > value:
                value = resultOfMinValue
    return value


def getMinValue(board):
    if terminal(board):
        return utility(board)
    else:
        value = math.inf
        for action in actions(board):
            resultOfMaxValue = getMaxValue(result(board, action))
            if resultOfMaxValue < value:
                value = resultOfMaxValue
    return value
