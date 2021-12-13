"""
"""

import chess
import numpy as np
from node import Node
import copy
import heuristics


'''
depth_limited_ab_search:

Similar to the textbook version, but Depth Limited Alpha Beta Search. 
Recursively called to go down the depth that set in the function call.

Parameters:
    - node - Node object, the current node
    - depth - int, the depth of the tree that is to be explored
    - alpha - float, the value of alpha, -infinity
    - beta - float, the value of beta, infinity
    - maximizing_player - Boolean, whether or not the current player is the maximizing player
    - curr_player - the current player, either B or W

Returns:
    returns the optimal move selected by the A/B search algorithm
'''

def depth_limited_ab_search(node, depth, alpha, beta, maximizing_player, curr_player):
    """
    Just like version from textbook except made recursive to do depth limited ab search
    """
    if depth == 0 or node.board_state.is_game_over():
        node.get_heuristic(curr_player)
        if node.move != "":
            return node.v, node.move
    if node.children == set():
        for next_move in list(node.board_state.legal_moves):
            new_board_state = copy.deepcopy(node.board_state)
            if node.kriegspiel:
                new_gt_board_state = copy.deepcopy(node.gt_board_state)
                if next_move not in new_gt_board_state.legal_moves:
                    continue
            else:
                new_gt_board_state = None

            next_move = next_move.uci()
            new_board_state.push_san(next_move)
            if node.kriegspiel:
                new_gt_board_state.push_san(next_move)

            child_node = Node(board_state=new_board_state, move=next_move, parent=node, kriegspiel=node.kriegspiel, gt_board_state=new_gt_board_state)
            if node.kriegspiel:
                child_node.update_opponent_pieces(curr_player, child_node.gt_board_state)
            else:
                child_node.v = heuristics.opponent_check(node.board_state, child_node.move, curr_player)
            node.children.add(child_node)
        if node.kriegspiel:
            node.get_diag_pawn_moves(curr_player)

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
        if move == -1:
            print("Move is -1", value)
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
        if move == -1:
            print("move is -1", value)
        return value, move
