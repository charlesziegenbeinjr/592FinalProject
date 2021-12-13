import chess
from node import Node
import numpy as np
import random
import sys
import heuristics

def ucb1(currentNode):
    return currentNode.v + np.sqrt(2) * \
        (np.sqrt(np.log(currentNode.N + np.exp(1) + (10**-7)) / (currentNode.n + (10**-11))))


def selection(currentNode): #SELECTION
    # if player == "white":
    selection = None
    ucb_value = -np.infty
    for child in currentNode.children:
        child_ucb = ucb1(child)
        if child_ucb > ucb_value:
            ucb_value = child_ucb
            selection = child
        return selection


def expansion(currentNode, player): #EXPANSION
    if len(currentNode.children) == 0:
        return currentNode
    if player == "white":
        descendant = selection(currentNode)
        return expansion(descendant, "black")
    if player == "black":
        descendant = selection(currentNode)
        return (expansion(descendant, "white"))


def playout(currentNode, depth): #ROLLOUT
    if currentNode.board_state.is_game_over():
        chessboard = currentNode.board_state
        if chessboard.result() == "1-0":
            return (currentNode, 1)
        elif chessboard.result() == "0-1":
            return (currentNode,0)
        else:
            return (currentNode,0.5)
    elif depth == 0:
        val = currentNode.get_heuristic("W", update_v=False)
        if val > 0:
            return (currentNode, 1)
        elif val < 0:
            return (currentNode, 0)
        else:
            return (currentNode, 0.5)

    legalMoves = list(currentNode.board_state.legal_moves)
    possibleMoves = [currentNode.board_state.san(i) for i in legalMoves]
    values = []
    for i in possibleMoves:
        descendant = Node()
        state = chess.Board(currentNode.board_state.fen())
        state.push_san(i)

        descendant.board_state = state
        descendant.parent = currentNode
        currentNode.children.add(descendant)
        val = descendant.get_heuristic("W", update_v=False)
        values.append(val+1)
    values = np.array(values, dtype="float64")
    if np.amin(values) < 0:
        values += -1*np.amin(values)
    rng = np.random.default_rng()
    return playout(random.choice(list(currentNode.children)), depth-1)
    



def backpropagate(currentNode, result): #BACKPROPAGATE
    currentNode.n += 1
    currentNode.v += result
    while currentNode.parent is not None:
        currentNode.N += 1
        currentNode = currentNode.parent
    return currentNode


def mcts(currentNode, kriegspiel=False):
    legalMoves = list(currentNode.board_state.legal_moves)
    possibleMoves = [currentNode.board_state.san(i) for i in legalMoves]
    move_map = dict()
    for i in possibleMoves:
        # Get FEN Notation of Board
        state = chess.Board(currentNode.board_state.fen())
        state.push_san(i) 
        descendant = Node()
        descendant.board_state = state
        descendant.parent = currentNode
        currentNode.children.add(descendant)
        move_map[descendant] = i

    sims = 200  # I.E "Until We Run Out of Time..."
    for sim_num in range(sims):
        child = selection(currentNode, "white", -np.infty)
        leaf = expansion(child, "white")
        finalNode, reward = playout(leaf, 0)
        currentNode = backpropagate(finalNode, reward)

    move = ''
    ucb_value = -np.infty
    for child in currentNode.children:
        child_ucb = ucb1(child)
        if child_ucb > ucb_value:
            ucb_value = child_ucb
            move = move_map[child]
    return move
