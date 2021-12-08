import chess
from node import Node
import numpy as np
import random
import sys
import heuristics


def ucb1(currentNode):
    return currentNode.v + np.sqrt(2) * \
        (np.sqrt(np.log(currentNode.N + np.exp(1) + (10**-7)) / (currentNode.n + (10**-11))))


def selection(currentNode, player, threshold, kriegspiel): #SELECTION
    if kriegspiel:
        selection = None
        ucb_value = threshold
        for child in currentNode.children:
            child_ucb = ucb1(child)
            if child_ucb > ucb_value:
                ucb_value = child_ucb
                selection = child
        return selection
    
    else:
        if player == "white":
            selection = None
            ucb_value = threshold
            for child in currentNode.children:
                child_ucb = ucb1(child)
                if child_ucb > ucb_value:
                    ucb_value = child_ucb
                    selection = child
            return selection
        
        if player == "black":
            selection = None
            ucb_value = threshold
            for child in currentNode.children:
                child_ucb = ucb1(child)
                if child_ucb < ucb_value:
                    ucb_value = child_ucb
                    selection = child
            return selection


def expansion(currentNode, player, kriegspiel, depth): #EXPANSION
    if kriegspiel:
        if not currentNode.children:
            return currentNode
        descendant = selection(currentNode, [], False)
        return expansion(descendant, kriegspiel)
    else:
        if len(currentNode.children) == 0 or depth == 0:
            return currentNode
        if player == "white":
            descendant = selection(currentNode, "white", -np.infty, kriegspiel)
            print("HERE1")
            return expansion(descendant, "black", kriegspiel, depth-1)
        if player == "black":
            print("HERE2")
            descendant = selection(currentNode, "black", np.infty, kriegspiel)
            return (expansion(descendant, "white", kriegspiel, depth-1))

def playout(currentNode, player): #ROLLOUT
    if currentNode.board_state.is_game_over():
        chessboard = currentNode.board_state
        if chessboard.result() == "1-0":
            return (currentNode, 1)
        elif chessboard.result() == "0-1":
            return (currentNode,0)
        else:
            return (currentNode,0.5)
    else:
        value = currentNode.get_heuristic(player)
        if value > 75:
            return currentNode, 1
        elif value < 75:
            return currentNode, 0
        else:
            return currentNode, 0.5
        # legalMoves = list(currentNode.board_state.legal_moves)
        # possibleMoves = [currentNode.board_state.san(i) for i in legalMoves]
        # for i in possibleMoves:
        # # Get FEN Notation of Board
        #     state = chess.Board(currentNode.board_state.fen())
        #     state.push_san(i)  # Push Move onto Move Stack
        #     descendant = Node()
        #     descendant.board_state = state
        #     descendant.parent = currentNode
        #     currentNode.children.add(descendant)
        # return playout(random.choice(list(currentNode.children)), "White")




def backpropagate(currentNode, result): #BACKPROPAGATE
    currentNode.n += 1
    currentNode.v += result
    while currentNode.parent is not None:
        currentNode.N += 1
        currentNode = currentNode.parent
    return currentNode


def mcts(currentNode, kriegspiel):
    legalMoves = list(currentNode.board_state.legal_moves)
    possibleMoves = [currentNode.board_state.san(i) for i in legalMoves]
    move_map = dict()
    for i in possibleMoves:
        # Get FEN Notation of Board
        state = chess.Board(currentNode.board_state.fen())
        state.push_san(i)  # Push Move onto Move Stack
        descendant = Node()
        descendant.board_state = state
        descendant.parent = currentNode
        currentNode.children.add(descendant)
        move_map[descendant] = i

    sims = 10  # I.E "Until We Run Out of Time..."
    depth = 5
    while (sims > 0):
        child = selection(currentNode, "white", -np.infty, kriegspiel)
        leaf = expansion(child, "black", kriegspiel, depth)
        finalNode, reward = playout(leaf, "white")
        currentNode = backpropagate(finalNode, reward)
        sims -= 1

    move = ''
    ucb_value = -np.infty
    for child in currentNode.children:
        child_ucb = ucb1(child)
        if child_ucb > ucb_value:
            ucb_value = child_ucb
            move = move_map[child]
    return move
