"""
FIXME

https://readthedocs.org/projects/python-chess/downloads/pdf/latest/
"""

import chess
import numpy as np
from enum import Enum
from alpha_beta_ai import depth_limited_ab_search
from mcts_ai import mcts
from node import Node
import copy
import utils
from tqdm import tqdm
from datetime import datetime

DEPTH = {"W": 2, "B": 2}


def setup_board(initial_setup=""):
    if initial_setup == "":
        return chess.Board()
    return chess.Board(initial_setup)

def host_game(initial_setup="", white="human", black="human", kriegspiel=False, print_updates=True, print_output=True):
    rng = np.random.default_rng()
    board = setup_board(initial_setup)
    curr_side = "W"
    while not board.outcome():
        curr_move = -1
        count = 0
        while curr_move == -1 or not chess.Move.from_uci(curr_move) in board.legal_moves:
            if count > 0 and print_updates:
                print("Invalid move, try again.")
            if (curr_side == "W" and white == "human") or (curr_side == "B" and black == "human"):
                curr_move = input(curr_side + ", make a move: ")
            else:
                if (curr_side == "W" and white == "random_ai") or (curr_side == "B" and black == "random_ai"):
                    if count == 0:
                        node = Node(board_state=copy.deepcopy(board), kriegspiel=kriegspiel)
                    if kriegspiel:
                        node.remove_opponent_pieces(curr_side)
                    if node.possible_moves == [] and kriegspiel:
                        node.get_diag_pawn_moves(curr_side)
                        node.possible_moves = list(node.board_state.legal_moves) + node.diag_pawn_moves

                    elif node.possible_moves == -1:
                        print("problem 1 found")
                        intersection = list(set(board.legal_moves) & set(list(node.board_state.legal_moves)+node.diag_pawn_moves))
                        print(intersection)

                    elif not kriegspiel:
                        node.possible_moves = list(node.board_state.legal_moves)

                    if node.possible_moves == -1:
                        print("hi")
                    move_idx = rng.choice(len(node.possible_moves))
                    curr_move = node.possible_moves[move_idx].uci()
                    node.possible_moves.remove(node.possible_moves[move_idx])

                    if node.possible_moves == []:
                        node.possible_moves = -1

                elif (curr_side == "W" and white == "alpha_beta_ai") or (curr_side == "B" and black == "alpha_beta_ai"):
                    if count == 0:
                        node = Node(board_state=copy.deepcopy(board), kriegspiel=kriegspiel, gt_board_state=copy.deepcopy(board))
                        if list(set(node.board_state.legal_moves) & set(board.legal_moves)) == []:
                            print("problem 2")
                    if kriegspiel:
                        node.remove_opponent_pieces(curr_side)
                        node.update_opponent_pieces(curr_side, board)
                    if count == 0:
                        value, curr_move = depth_limited_ab_search(node, DEPTH[curr_side], -np.infty, np.infty, True, curr_side)
                    else:
                        value, curr_move = node.get_nth_best_move(count, curr_side)
                        if len(curr_move) == 0:
                            print("uh oh 3")


                elif (curr_side == "W" and white == "mcts_ai") or (curr_side == "B" and black == "mcts_ai"):
                    node = Node(board_state=copy.deepcopy(board), kriegspiel=kriegspiel, gt_board_state=copy.deepcopy(board))
                    if kriegspiel:
                        node.remove_opponent_pieces(curr_side)
                        node.update_opponent_pieces(curr_side, board)
                    try:
                        curr_move = board.parse_san(mcts(node)).uci()
                    except ValueError:
                        value, curr_move = node.get_nth_best_move(count, curr_side)


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
            print()
            utils.pretty_print_board(board)
            print()
        # if board.fullmove_number > 10:
        #     break
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
    # host_game(white="alpha_beta_ai", black="random_ai")
    start = datetime.now()
    for i in tqdm(range(10)):
        host_game(white="mcts_ai", black="random_ai", kriegspiel=False,print_updates=False, print_output=True)
    end = datetime.now()
    print("Total time:", end-start)
if __name__ == "__main__":
    main()
