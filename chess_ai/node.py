"""
"""
import chess
import numpy as np
import heuristics
import utils
import copy

class Node:
    def __init__(self, board_state=chess.Board(), move="", parent=None, kriegspiel=False, opponent_pieces=None, gt_board_state=None):
        self.board_state = board_state
        self.move = move
        self.children = set()
        self.parent = parent
        self.N = 0
        self.n = 0
        self.v = 0
        self.possible_moves = []
        self.sorted_children = []
        self.diag_pawn_moves = []
        self.kriegspiel = kriegspiel
        self.opponent_pieces = opponent_pieces
        self.gt_board_state = gt_board_state

    def get_heuristic(self, curr_player, update_v=True):
        val = 0
        if self.kriegspiel:
            val = heuristics.get_material_value(self.board_state, curr_player, self.kriegspiel, self.opponent_pieces)
        else:
            val = heuristics.get_material_value(self.board_state, curr_player, self.kriegspiel, self.opponent_pieces) - \
                     heuristics.count_attacks(self.board_state, curr_player)
        if update_v:
            self.v += val
            # if type(self.v) == type(1):
            #     self.v += val
            # else:
            #     self.v = val
        return val


    def remove_opponent_pieces(self, curr_player):
        board_array = utils.get_board_state_array(self.board_state)
        cols = chess.FILE_NAMES
        for row in range(8):
            for col in range(8):
                if board_array[row][col] == ".":
                    continue
                elif (board_array[row][col].isupper() and curr_player=="B") or \
                     (board_array[row][col].islower() and curr_player=="W"): # current player is black and want to remove white pieces
                    self.board_state.remove_piece_at(8*(7-row)+col)

    def get_diag_pawn_moves(self, curr_player):
        board_array = utils.get_board_state_array(self.board_state)
        for row in range(8):
            for col in range(8):
                curr_pos = chess.FILE_NAMES[col] + str(8-row)
                if board_array[row][col] == ".":
                    continue
                elif board_array[row][col] == "P" and curr_player == "W":
                    if (row - 1) >= 0 and (col - 1) >= 0:
                        diag_move = curr_pos + chess.FILE_NAMES[col-1] + str(8 - (row - 1))
                        self.diag_pawn_moves.append(chess.Move.from_uci(diag_move))
                    if (row - 1) >= 0 and (col + 1) <= 7:
                        diag_move = curr_pos + chess.FILE_NAMES[col+1] + str(8 - (row - 1))
                        self.diag_pawn_moves.append(chess.Move.from_uci(diag_move))
                elif board_array[row][col] == "p" and curr_player == "B":
                    if (row + 1) <= 7 and (col - 1) >= 0:
                        diag_move = curr_pos + chess.FILE_NAMES[col-1] + str(8 - (row + 1))
                        self.diag_pawn_moves.append(chess.Move.from_uci(diag_move))
                    if (row + 1) <= 7 and (col + 1) <= 7:
                        diag_move = curr_pos + chess.FILE_NAMES[col+1] + str(8 - (row + 1))
                        self.diag_pawn_moves.append(chess.Move.from_uci(diag_move))

    def get_nth_best_move(self, n, curr_player):
        if self.children == set():
            for next_move in list(self.board_state.legal_moves):
                new_board_state = copy.deepcopy(self.board_state)
                if self.kriegspiel:
                    new_gt_board_state = copy.deepcopy(self.gt_board_state)
                    if next_move not in new_gt_board_state.legal_moves:
                        continue
                else:
                    new_gt_board_state = None
                next_move = next_move.uci()
                new_board_state.push_san(next_move)
                if self.kriegspiel:
                    new_gt_board_state.push_san(next_move)
                child_node = Node(board_state=new_board_state, move=next_move, parent=self, kriegspiel=self.kriegspiel, gt_board_state=new_gt_board_state)
                if node.kriegspiel:
                    child_node.update_opponent_pieces(curr_player, child_node.gt_board_state)
                else:
                    child_node.v = heuristics.opponent_check(node.board_state, child_node.move, curr_player)
                self.children.add(child_node)
            if self.kriegspiel:
                self.get_diag_pawn_moves(curr_player)
        if self.sorted_children == []:
            children_lst = []
            children_v = []
            for child_node in self.children:
                if child_node.v == 0:
                    child_node.get_heuristic(curr_player)
                children_v.append(child_node.v)
                children_lst.append(child_node)
            children_lst = np.array(children_lst)
            children_v = np.array(children_v)
            idx = np.argsort(children_v)
            sorted_values = children_v[idx]
            self.sorted_children = list(children_lst[idx])


            for i in range(len(children_lst)):
                if self.sorted_children[i].v != sorted_values[i]:
                    print("uh oh")
        if self.sorted_children == -1:
            if self.diag_pawn_moves == []:
                print("hm")
                print("problem 2, found")
            next_move = self.diag_pawn_moves.pop()
            next_move = next_move.uci()
            return self.v, next_move

            #
            # return -1, -1
        else:
            #print(n, len(self.sorted_children))
            selected_child = self.sorted_children.pop(-1)
            if self.sorted_children == []:
                self.sorted_children = -1
            #print(len(self.sorted_children))
            return selected_child.v, selected_child.move

        # if n > len(children_lst):
        #     return sorted_children[0].v, sorted_children[0].move
        # return sorted_children[-n].v, sorted_children[-n].move

    def update_opponent_pieces(self, curr_player, full_board_state):
        self.opponent_pieces = {}
        board_array = utils.get_board_state_array(full_board_state)
        for row in range(8):
            for col in range(8):
                if board_array[row][col] == ".":
                    continue
                elif (board_array[row][col].isupper() and curr_player=="B") or \
                     (board_array[row][col].islower() and curr_player=="W"): # current player is black and want to remove white pieces
                    piece = board_array[row][col].lower()
                    if piece not in self.opponent_pieces:
                        self.opponent_pieces[piece] = 1
                    else:
                        self.opponent_pieces[piece] += 1
