"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

emptyCount = 0
XCount = 0
OCount = 0

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def lookInBoard(board):
    """
     Looks through the board and counts the number of X's , O's 
     and enpty spaces i the board
     """
    global emptyCount,XCount,OCount
    emptyCount = 0
    XCount = 0
    OCount = 0

    for i in range(3):
        for j in range(3):
            if board[i][j]==EMPTY:
                    emptyCount += 1
            elif board[i][j]==X:
                    XCount += 1
            elif board[i][j]==O:
                    OCount += 1 


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    lookInBoard(board)

    if emptyCount != 0:
        if XCount == OCount:
            return X

        else:
            return O

    else:
        return None


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    if terminal(board) == False:
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    action = (i,j)
                    actions.add((action))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    boardCopy = copy.deepcopy(board)
    
    if action[0] > 2 or action [1] > 2:
        raise Exception('InvalidAction')
    else:
        row = action[0]
        column = action[1]
        
        if player(board) == X:
            boardCopy[row][column] = X
        else:
            boardCopy[row][column] = O

    return boardCopy        




def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner = None
    
    row1 = board[0][0]==board[0][1]==board[0][2]!= None
    row2 = board[1][0]==board[1][1]==board[1][2]!= None
    row3 = board[2][0]==board[2][1]==board[2][2]!= None

    if row1:
        winner = board[0][0]
    elif row2:
        winner = board[1][0]
    elif row3:
        winner = board[2][0]

    col1 = board[0][0]==board[1][0]==board[2][0]!= None
    col2 = board[0][1]==board[1][1]==board[2][1]!= None
    col3 = board[0][2]==board[1][2]==board[2][2]!= None

    if col1:
        winner = board[0][0]
    elif col2:
        winner = board[0][1]
    elif col3:
        winner = board[0][2]

    diag1 = board[0][0]==board[1][1]==board[2][2]!= None
    diag2 = board[0][2]==board[1][1]==board[2][0]!= None
    
    if diag1:
        winner = board[0][0]
    elif diag2:
        winner = board[0][2]

    return winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    Winner = winner(board)

    lookInBoard(board)
                        
    if emptyCount == 0 or Winner == X or Winner == O:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    Winner = winner(board)

    if Winner == X:
        return 1
    elif Winner == O:
        return -1 
    elif Winner == None:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    elif player(board) == X:
        bestValue = -2
        moves = []
        for action in actions(board):
            moveValue = minValue(result(board, action))
            if moveValue == 1:
                return action
            elif moveValue > bestValue:
                bestValue = moveValue
                moves.clear()
                moves.append(action)
        return moves[0]

    elif player(board) == O:
        bestValue = 2
        moves = []
        for action in actions(board):
            moveValue = maxValue(result(board, action))
            if moveValue == -1:
                return action
            elif moveValue < bestValue:
                bestValue = moveValue
                moves.clear()
                moves.append(action)
        return moves[0]


def maxValue(board):
    
    if terminal(board):
        return utility(board)

    value = -2
    for action in actions(board):
        value = max(value,minValue(result(board,action)))
        if value == 1:
            break
    return value
        
        
def minValue(board):
    
    if terminal(board):
        return utility(board)

    value = 2
    for action in actions(board):
        value = min(value,maxValue(result(board,action)))
        if value == -1:
            break
    return value
