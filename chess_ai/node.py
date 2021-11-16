"""
"""
import chess
import numpy as np
import heuristics

class Node:
    def __init__(self, board_state=chess.Board(), move="", parent=None):
        self.board_state = board_state
        self.move = move
        self.children = set()
        self.parent = parent
        # self.N = 0
        # self.n = 0
        self.v = 0#np.random.randint(10)

    def get_heuristic(self, curr_player):
        self.v = heuristics.get_material_value(self.board_state, curr_player)
        # eventually will call multiple heuristic functions
