"""
Tic Tac Toe Player
"""

from json.encoder import INFINITY
import math
from multiprocessing.sharedctypes import Value

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
    x_count = 0
    o_count = 0
    #if it is the initial state, X starts
    if board == [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]:
        return X
    #count number of X
    #count number of O
    for row in board:
        for item in row:
            if item == X:
                x_count += 1
            elif item == O:
                o_count += 1
    #determinar el movimiento
    if x_count > o_count:
        return O
    elif x_count < o_count:
        return X
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set() #set of possible actions
    i=0
    j=0
    for row in board:
        for item in row:
            if item == None:
                actions.add((i,j))
            j += 1
        i +=1
        j=0
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    (i,j) = action
    if i<0 or i>=3 or j<0 or j>=3:
        raise ValueError('action not correct')
    new_board = [row[:] for row in board]
    new_board[i][j] = player(board)
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    diagonal1 = []
    diagonal2 = []
    #check horizontally
    for row in board:
        if row.count(X) == 3:
            return X
        elif row.count(O) == 3:
            return O
    #check vertical
    for i in range(len(board)):
        vertical = []
        for j in range(len(board)):
            vertical.append(board[j][i])
        if all(elem==X for elem in vertical):
            return X
        elif all(elem==O for elem in vertical):
            return O
    #check diagonales
    for i in range(len(board)):
      diagonal1.append(board[i][i])
      diagonal2.append(board[i][len(board)-i-1])
    if all(elem==X for elem in diagonal1):
        return X
    elif all(elem==O for elem in diagonal1):
        return O
    elif all(elem==X for elem in diagonal2):
        return X
    elif all(elem==O for elem in diagonal2):
        return O
    
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #print(winner(board))
    if winner(board) != None:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)
    if result == X:
        return 1
    elif result == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)
    if terminal(board):
        return None
    #print(current_player
    elif current_player == X:
        explored_actions = {}
        for action in actions(board):
            explored_actions[action] = minvalue(result(board, action))
            print(explored_actions)
        return max(explored_actions, key=explored_actions.get)
    elif current_player == O:
        explored_actions = {}
        for action in actions(board):
            explored_actions[action] = maxvalue(result(board, action))
            print(explored_actions)
        return min(explored_actions, key=explored_actions.get)
    
def maxvalue(board):
    if terminal(board):
        return utility(board)
    v = -1
    possible_actions = actions(board)
    for action in possible_actions:
        v = max(v,minvalue(result(board,action)))
    return v
    
def minvalue(board):
    if terminal(board):
        return utility(board)
    v = 1
    possible_actions = actions(board)
    for action in possible_actions:
        v = min(v,maxvalue(result(board,action)))
    return v

"""
board = [[X, O, O],
        [X, O, O],
        [O, None, X]]

print(terminal(board))

"""
