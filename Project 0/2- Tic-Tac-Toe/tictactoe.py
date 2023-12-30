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
    # If board is empty, X player start the game
    if board is None:
        return X
    else:
        times_played = 0
        # Iterate over the board to count the times played
        for line in board:
            for column in line:
                if column is not None:
                    times_played += 1
                    
        # If the times played is even, is X turn, O otherwise
        if times_played % 2 == 0:
            return X
        else:
            return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Set of possible actions
    possible_actions = set()

    # Iterate over the board to look for possible actions
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is EMPTY:
                possible_actions.add((i, j))
                
    return possible_actions

    
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    possible_actions = actions(board)
    
    # If the action is not valid, raise an exception
    if action not in possible_actions:
        raise Exception("Invalid Action!")
    
    # Create a deep copy of the board to modify it
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Horizontal winning
    for i in range(len(board)):
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] == X:
                return X
            elif board[i][0] == O:
                return O
            
    # Vertical winning
    for j in range(len(board)):
        if board[0][j] == board[1][j] == board[2][j]:
            if board[0][j] == X:
                return X
            elif board[0][j] == O:
                return O
    
    # Diagonally winning
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O
    elif board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] == X:
            return X
        elif board[0][2] == O:
            return O
            
    # If not winning yet return None
    return None
            

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if there is not possible actions or any player already won
    if not actions(board) or (winner(board) == X or winner(board) == O):
        return True  
    # Game is not finished
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If the game is over return None
    if terminal(board):
        return None

    if player(board) == X:
        v = -math.inf
        best_move = None
        for action in actions(board):
            max_value = Min_Value(result(board, action))
            if max_value > v:
                v = max_value
                best_move = action
        return best_move
        
    else:
        v = math.inf
        best_move = None
        for action in actions(board):
            min_value = Max_Value(result(board, action))
            if min_value < v:
                v = min_value
                
                best_move = action
        return best_move

    
def Max_Value(board):
    if terminal(board):
        return utility(board)
    
    v = -math.inf    
    for action in actions(board):
        v = max(v, Min_Value(result(board, action)))
        
    return v

def Min_Value(board):
    if terminal(board):
        return utility(board)
    
    v = math.inf
    for action in actions(board):
        v = min(v, Max_Value(result(board, action)))
        
    return v