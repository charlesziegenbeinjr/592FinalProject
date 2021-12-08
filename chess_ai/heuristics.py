import chess
import numpy as np
import utils

PIECE_VALUES = {"p": 1, "b": 3, "n": 3, "r": 5, "q": 9, "k": 0}


def get_material_value(board_state, curr_player, kriegspiel=False, opponent_pieces=None, weight=1): # how much to weight this heuristic
    board_array = utils.get_board_state_array(board_state)
    white_points = 0
    black_points = 0

    for row in range(8):
        for col in range(8):
            if board_array[row][col] == ".":
                continue
            elif kriegspiel:
                if board_array[row][col].isupper() and curr_player == "W":
                    white_points += PIECE_VALUES[board_array[row][col].lower()]
                elif board_array[row][col].islower() and curr_player == "B":
                    black_points += PIECE_VALUES[board_array[row][col]]
            else:
                if board_array[row][col].isupper():
                    white_points += PIECE_VALUES[board_array[row][col].lower()]
                elif board_array[row][col].islower():
                    black_points += PIECE_VALUES[board_array[row][col]]
    # black_pts = 0
    # kriegspiel_white_pts = 0
    if kriegspiel:
        for piece in opponent_pieces:
            if curr_player == "W":
                black_points += PIECE_VALUES[piece] * opponent_pieces[piece]
            else:
                white_points += PIECE_VALUES[piece] * opponent_pieces[piece]
    if curr_player == "W":
        return (white_points - black_points) * weight
    return (black_points - white_points) * weight




"""
Want to use a lot of the information below to inform heuristic value
"""

def count_attacks(board_state, curr_player):
    board_array = utils.get_board_state_array(board_state)
    num_pieces_attacked = 0
    for row in range(8):
        for col in range(8):
            piece = board_array[row][col]
            pos = 8*(7-row)+col
            if board_array[row][col] == ".":
                continue
            if piece.isupper() and curr_player == "W" and board_state.is_attacked_by(chess.BLACK, pos):
                num_pieces_attacked += 1
            elif piece.islower() and curr_player == "B" and board_state.is_attacked_by(chess.WHITE, pos):
                num_pieces_attacked += 1
    return num_pieces_attacked

def opponent_check(board_state, move, curr_player):
    if board_state.gives_check(chess.Move.from_uci(move)):
        return 100
    else:
        return 0



# def attacked(board_state, curr_player):
#     board.is_check()
#     attackers = board.attackers(chess.WHITE, chess.F3)



# checkers() → chess.SquareSet
# Gets the pieces currently giving check.
# Returnsaset of squares. is_check() → bool
# Tests if the current side to move is in check.
# gives_check(move: chess.Move) → bool
# Probes if the given move would put the opponent in check. The move must be at least pseudo-legal.

# peek()
# Gets the last move from the move stack.

#
# is_en_passant(move: chess.Move) → bool
# Checks if the given pseudo-legal move is an en passant capture.
# is_capture(move: chess.Move) → bool
# Checks if the given pseudo-legal move is a capture.
# is_zeroing(move: chess.Move) → bool
# Checks if the given pseudo-legal move is a capture or pawn move.
# is_irreversible(move: chess.Move) → bool Checks if the given pseudo-legal move is irreversible.
# In standard chess, pawn moves, captures, moves that destroy castling rights and moves that cede en passant are irreversible.
# This method has false-negatives with forced lines. For example, a check that will force the king to lose castling rights is not considered irreversible. Only the actual king move is.
