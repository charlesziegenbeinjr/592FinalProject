import chess
import numpy as np
from termcolor import colored

'''
Get the state of the board in the form of an list

Parameters:
    - board_state - python-chess's BoardState, the chessboard state

Returns:
    Returns the board state in list form instead of a full-fledged chess notation
'''
def get_board_state_array(board_state):
    board_array = []
    for row in str(board_state).split("\n"):
        board_array.append(row.split(" "))
    return np.array(board_array)

'''
Prints the chessboard in a pretty way

Parameters:
    - board_state - python-chess's BoardState, the chessboard state

Returns:
    Void return, prints out the board in the format defined by the function.
'''
def pretty_print_board(board_state):
    board_array = get_board_state_array(board_state)
    letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
    for row in range(9):
        for col in range(8):
            if col == 0:
                if row != 8:
                    print(8-row, end=" ")
                else:
                    print("  ", end="")
            if row < 8:
                if board_array[row][col] == ".":
                    print(board_array[row][col], end=" ")
                elif board_array[row][col].isupper():
                    print(colored(board_array[row][col], "magenta"), end=" ")
                else:
                    print(colored(board_array[row][col], "cyan"), end=" ")
            else:
                print(letters[col], end=" ")

        print()
