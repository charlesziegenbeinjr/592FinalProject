"""
FIXME
"""

import chess
import numpy as np
from enum import Enum
from alpha_beta_ai import depth_limited_ab_search
from mcts_ai import mcts
from node import Node
import copy

DEPTH = 2


def setup_board(initial_setup=""):
    if initial_setup == "":
        return chess.Board()
    return chess.Board(initial_setup)

def host_game(initial_setup="", white="human", black="human", print_updates=True, print_output=True):
    rng = np.random.default_rng()
    board = setup_board(initial_setup)
    curr_side = "W"
    while not board.outcome():
        curr_move = -1
        count = 0
        while curr_move == -1 or not chess.Move.from_uci(curr_move) in board.legal_moves:
            if count > 0:
                print("Invalid move, try again.")
            if (curr_side == "W" and white == "human") or (curr_side == "B" and black == "human"):
                curr_move = input(curr_side + ", make a move: ")
            else:
                if (curr_side == "W" and white == "random_ai") or (curr_side == "B" and black == "random_ai"):
                    print("HERE")
                    possible_moves = list(board.legal_moves)
                    move_idx = rng.choice(len(possible_moves))
                    curr_move = possible_moves[move_idx].uci()
                elif (curr_side == "W" and white == "alpha_beta_ai") or (curr_side == "B" and black == "alpha_beta_ai"):
                    node = Node(board_state=copy.deepcopy(board))
                    value, curr_move = depth_limited_ab_search(node, DEPTH, -np.infty, np.infty, True, curr_side)
                elif (curr_side == "W" and white == "mcts_ai") or (curr_side == "B" and black == "mcts_ai"):
                    node = Node(board_state=copy.deepcopy(board))
                    curr_move = board.parse_san(mcts(node)).uci()
                else:
                    print("Invalid AI type")
                    return
                if print_updates:
                    print(curr_side + "'s move:", curr_move)
            count += 1
        board.push_san(curr_move)
        if curr_side == "W":
            curr_side = "B"
        else:
            curr_side = "W"
        if print_updates:
            print(board)
    game_outcome = board.outcome()
    game_termination = game_outcome.termination.name
    if print_output:
        if game_termination == "CHECKMATE":
            winner = game_outcome.winner
            if winner:
                print("Outcome: CHECKMATE, W wins")
            else:
                print("Outcome: CHECKMATE, B wins")
        else:
            print("Outcome:", game_termination)
        print("Number of moves:", board.fullmove_number)
    return game_outcome.result()


def main():
    # host_game(white="alpha_beta_ai", black="alpha_beta_ai")
    host_game(white="mcts_ai", black="random_ai")
if __name__ == "__main__":
    main()
