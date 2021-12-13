import chess
import numpy as np
import utils

PIECE_VALUES = {"p": 1, "b": 3, "n": 3, "r": 5, "q": 9, "k": 0}

'''
get_material_value:

Gets the material value of a players pieces based on the number of player and opponent pieces

Parameters:
    - board_state - python-chess's BoardState, the current chessboard
    - curr_player - String, either "W" or "B"
    - kriegspiel - Boolean, whether we are playing kriegspiel or not
    - opponent_pieces - List, for kriegspiel to get the opponent pieces on the board
    - weight - Int, how much to weight the heuristic

Returns:
    Based on the player, returns (PlayerPoints - OpponentsPoints) * weight based on the calculations
    from the values of the remaining pieces from each player
'''
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

'''
count_attacks:

Counts the total number of pieces that can be attacked based on the setup of the board
and the player whose turn it is

Parameters:
    - board_state - python-chess BoardState, the current status of the chessboard
    - curr_player - String, the current player "W" or "B"

Returns:
    The number of pieces that can be attacked based on the chessboard setup and the current player
    based on their remaining pieces
'''
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

'''
opponent_check:

If a move puts an opponent in check, incentivize the mode by providing it with a hgih reward.

Parameters:
    - board_state - python-chess BoardState, the current status of the chessboard
    - move - String, the move to be taken in UCI format
    - curr_player - String, the current player "W" or "B"

Returns:
    Returns the extra reward meant to incentivize putting the opponent king in check, either
    100 (for check) or 0 (no check). 
'''
def opponent_check(board_state, move, curr_player):
    if board_state.gives_check(chess.Move.from_uci(move)):
        return 100
    else:
        return 0
