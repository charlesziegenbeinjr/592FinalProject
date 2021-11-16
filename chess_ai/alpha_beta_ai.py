"""
"""

import chess
import numpy as np
from node import Node
import copy
import heuristics



def depth_limited_ab_search(node, depth, alpha, beta, maximizing_player, curr_player):
    """
    Just like version from textbook except made recursive to do depth limited ab search
    """
    if depth == 0 or node.board_state.is_game_over():
        node.get_heuristic(curr_player)
        return node.v, node.move
    if node.children == set():
        for next_move in list(node.board_state.legal_moves):
            new_board_state = copy.deepcopy(node.board_state)
            next_move = next_move.uci()
            new_board_state.push_san(next_move)
            child_node = Node(board_state=new_board_state, move=next_move, parent=node)
            node.children.add(child_node)
    if maximizing_player:
        value = -np.infty
        move = -1
        for child_node in node.children:
            new_value, new_move = depth_limited_ab_search(child_node, depth-1, alpha, beta, False, curr_player)
            if new_value > value:
                value = new_value
                move = child_node.move
                alpha = max(alpha, value)
            if value >= beta:
                return value, move
        return value, move
    else:
        value = np.infty
        move = -1
        for child_node in node.children:
            new_value, new_move = depth_limited_ab_search(child_node, depth-1, alpha, beta, True, curr_player)
            if new_value < value:
                value = new_value
                move = child_node.move
                beta = min(beta, value)
            if value <= alpha:
                return value, move
        return value, move
