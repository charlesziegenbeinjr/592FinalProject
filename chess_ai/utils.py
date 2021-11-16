import chess
import numpy as np


def get_board_state_array(board_state):
    board_array = []
    for row in str(board_state).split("\n"):
        board_array.append(row.split(" "))
    return np.array(board_array)
