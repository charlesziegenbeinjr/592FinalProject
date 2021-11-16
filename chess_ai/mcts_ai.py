import chess
from node import Node
import numpy as np
import random
import sys


def ucb1(currentNode):
    return currentNode.v + np.sqrt(2) * \
        (np.sqrt(np.log(currentNode.N + np.exp(1) + (10**-7)) / (currentNode.n + (10**-11))))


def selection(currentNode, mapping, endGame):
    max = -np.infty
    selection = None
    move = ''
    for child in currentNode.children:
        child_ucb = ucb1(child)
        if child_ucb > max:
            max = child_ucb
            if endGame:
                move = mapping[child]
            selection = child
    if endGame:
        return move
    else:
        return selection


def expansion(currentNode):
    if not currentNode.children:
        return currentNode
    descendant = selection(currentNode, [], False)
    return expansion(descendant)


def playout(currentNode):
    if not currentNode.board_state.is_game_over():
        legalMoves = list(currentNode.board_state.legal_moves)
        possibleMoves = [currentNode.board_state.san(i) for i in legalMoves]
        for i in possibleMoves:
            # Get FEN Notation of Board
            state = chess.Board(currentNode.board_state.fen())
            state.push_san(i)  # Push Move onto Move Stack
            descendant = Node()
            descendant.board_state = state
            descendant.parent = currentNode
            currentNode.children.add(descendant)
        return playout(random.choice(list(currentNode.children)))
    else:
        chessboard = currentNode.board_state
        if chessboard.result() == "1-0":
            return 1
        elif chessboard.result() == "0-1":
            return -1
        else:
            return 0


def backpropagate(currentNode, result):
    currentNode.n += 1
    currentNode.v += result
    while currentNode.parent is not None:
        currentNode.N += 1
        currentNode = currentNode.parent
    return currentNode


def mcts(currentNode):
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

    sims = 2  # I.E "Until We Run Out of Time..."
    while (sims > 0):
        leaf = selection(currentNode, move_map, False)
        child = expansion(leaf)
        reward = playout(child)
        currentNode = backpropagate(child, reward)
        sims -= 1


    move = selection(currentNode, move_map, True)
    return move