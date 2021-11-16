"""
https://python-chess.readthedocs.io/en/latest/
"""

import chess
import numpy as np
import copy

board = chess.Board()
print(board)


print(board.legal_moves)

#print(chess.Move.from_uci("xxxx") in board.legal_moves)

board.push_san("e2e4") # move =

board_array = []
for row in str(board).split("\n"):
    board_array.append(row.split(" "))
board_array = np.array(board_array)
print(board_array.shape)
print(board_array)

# temp = str(board)
# print(len(temp))
# print(temp.split("\n"))
# length = 0
# for i in temp.split("\n"):
#     length += len(i)
# print(length)
# for i in temp:
#     print(i)
#print(type(board))

board2 = copy.deepcopy(board)
board.push_san("e5")
# print(board)
board.push_san("Qh5")
board.push_san("Nc6")
board.push_san("Bc4")
board.push_san("Nf6")
board.push_san("Qxf7")
print()
# print(board2)
# print(board.is_checkmate())
# print(board.outcome())
# print(board)
# board.push_san("e5")
