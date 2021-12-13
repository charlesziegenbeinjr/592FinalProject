"""
"""
import chess
import numpy as np
import heuristics
import utils
import copy

'''
Classes:
    Node
        Established to create objects that populate the search trees used by 
        MCTS and AB Search algorithms.
        
        Properties:
            - board_state: the state of the python-chess chessboard for the Node
            - move: the physical move associated with the object
            - children: the child nodes from the object, I.E the child moves 
            that are possible from the currentNode
            - parent: the parent node of the object
            - N: number of visits to the parent of current node
            - v: winning score of current node
            - n: number of visits to the current node
            - possible_moves: holds possible moves from current node
            - sorted_children: sorted list containing children of current node
            - diag_pawn_moves: diagonal pawn moves that can be made from current node
            - kriegspiel: T/F as to if we are playing Kriegspiel or normal chess,
            respectively
            - opponent_pieces: uses the ground truth board state to figure out which 
            opponent pieces still remain on the board (specifically how many of each type.
             something a kriegspiel player would be able to deduce from capture messages from the
             referee.
            - gt_board_state: ground truth board state (both sides of board). 
            Used for error checking and getting umpire messages 
'''

class Node:

    '''
    Establishes the Object with properties passed in
                
    Parameters: 
        board_state - BoardState, the current chessboard from python-chess
        parent - None, no parents yet
        move - String, empty string, changed during play
        kriegspiel - Boolean, depending on what variant we are playing
        opponent_pieces - List, None to start, will include which opponent pieces remain
        from the ground_truth board
        gt_board_state - BoardState, None to start, ground_truth_board simulating umpire messages
    
    Returns:
        A new object of class Node
    '''
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
    
    '''
    Node.get_heuristic:

    Returns the value computed by the heuristic for both Kriegspiel and 
    Regular chess

    Parameters:
        curr_player - the current player, W or B
        update_v - Boolean, updates the win/loss of current node
        when set to True

    Returns:
        the heuristic value for the node
    '''
    def get_heuristic(self, curr_player, update_v=True):
        val = 0
        if self.kriegspiel:
            val = heuristics.get_material_value(self.board_state, curr_player, self.kriegspiel, self.opponent_pieces)
        else:
            val = heuristics.get_material_value(self.board_state, curr_player, self.kriegspiel, self.opponent_pieces) - \
                     heuristics.count_attacks(self.board_state, curr_player)
        if update_v:
            self.v += val
        return val

    '''
    Node.remove_opponent_pieces:

    For Kriegspiel, removes the opponents pieces from the legal_moves array when playing Kriegspiel

    Parameters:
        curr_player - the current player, I.E whose turn it is when this function is called
    
    Returns:
        Void return, instead removes pieces on the board_state of the node
    '''
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

    '''
    Node.get_diag_pawn_moves:

    For Kriegspiel, an edge case state when we need to get the number of diagonal pawn moves that can be made.
    Given the setup of Kriegspiel, not knowing where the opponent's pieces are can make python-chess think there aren't 
    legal moves remaining, so this checks to see if a pawn capture can be made, as diagonal pawn moves aren't legal unless
    it is a legal capture move

    Parameters:
        curr_player - the current player, I.E whose turn it is when this function is called

    Returns:
        Void return, instead adds potential diagonal pawn moves for capture to the diag_pawn_moves property of the current node
    '''
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

    '''
    Node.get_nth_best_move:

    Returns the nth best move according to the search algorithm where n is the number of move attempts

    Parameters:
        n - Int, number of move attempts
        curr_player - the current player, I.E whose turn it is when this function is called
    
    Returns:
        Int, returns the nth best move according to the search algorithm where n is the number of move attempts
    '''
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

        else:
            selected_child = self.sorted_children.pop(-1)
            if self.sorted_children == []:
                self.sorted_children = -1
            return selected_child.v, selected_child.move

    '''
    Node.update_opponent_pieces

    opponent_pieces is the dictionary that maps piece type to the number of 
    opponent pieces of that type remaining

    Parameters:
        curr_player - the current player, I.E whose turn it is when this function is called
        full_board_state - the entire chessboard

    Returns:
        an update to the opponent_pieces dictionary
    '''
    def update_opponent_pieces(self, curr_player, full_board_state):
        self.opponent_pieces = {}
        board_array = utils.get_board_state_array(full_board_state)
        for row in range(8):
            for col in range(8):
                if board_array[row][col] == ".":
                    continue
                elif (board_array[row][col].isupper() and curr_player=="B") or \
                     (board_array[row][col].islower() and curr_player=="W"): 
                    piece = board_array[row][col].lower()
                    if piece not in self.opponent_pieces:
                        self.opponent_pieces[piece] = 1
                    else:
                        self.opponent_pieces[piece] += 1
