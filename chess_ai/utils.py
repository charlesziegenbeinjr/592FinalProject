import chess
import numpy as np
from termcolor import colored


def get_board_state_array(board_state):
    board_array = []
    for row in str(board_state).split("\n"):
        board_array.append(row.split(" "))
    return np.array(board_array)

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
