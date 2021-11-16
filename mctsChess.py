# Chess Libraries
import chess
import chess.pgn
# Ease of MCTS
import numpy as np
import random


class node():
    def __init__(self):
        self.state = chess.Board()  # Current Status of Board
        self.children = set()  # Legal Actions from Current Node
        self.parent = None  # Parent Node of Current Node
        self.N = 0  # Number of Playouts Through Current Node
        self.n = 0  # Number of Visits to Current Node
        self.v = 0  # Exploitation term, average utility of n


def ucb1(currentNode):
    return currentNode.v + np.sqrt(2) * \
        (np.sqrt(np.log(currentNode.N + np.exp(1) + (10**-7)) / (currentNode.n + (10**-11))))

def selection(currentNode, mapping, endGame):
    max = np.NINF
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
    descendant = selection(currentNode,[],False)
    return expansion(descendant)

def playout(currentNode):
    if not currentNode.state.is_game_over():
        legalMoves = list(currentNode.state.legal_moves)
        possibleMoves = [currentNode.state.san(i) for i in legalMoves]
        for i in possibleMoves:
            # Get FEN Notation of Board
            state = chess.Board(currentNode.state.fen())
            state.push_san(i)  # Push Move onto Move Stack
            descendant = node()
            descendant.state = state
            descendant.parent = currentNode
            currentNode.children.add(descendant)
        return playout(random.choice(list(currentNode.children)))
    else:
        chessboard = currentNode.state
        if chessboard.result() == "1-0":
            return 1
        elif chessboard.result() == "0-1":
            return 0
        else:
            return -1


def backpropagate(currentNode, result):
    currentNode.n += 1
    currentNode.v += result
    while currentNode.parent is not None:
        currentNode.N += 1
        currentNode = currentNode.parent
    return currentNode


def mcts(currentNode, mcts_player):
    legalMoves = list(currentNode.state.legal_moves)
    possibleMoves = [currentNode.state.san(i) for i in legalMoves]
    move_map = dict()
    for i in possibleMoves:
        state = chess.Board(currentNode.state.fen()) # Get FEN Notation of Board
        state.push_san(i) # Push Move onto Move Stack
        descendant = node()
        descendant.state = state
        descendant.parent = currentNode
        currentNode.children.add(descendant)
        move_map[descendant] = i
    
    sims = 10 # I.E "Until We Run Out of Time..."
    while (sims > 0):
        if mcts_player:
            leaf = selection(currentNode, move_map, False)
            child = expansion(leaf)
            reward = playout(child)
            currentNode = backpropagate(child, reward)
            sims -= 1
        else:
            break
    
    if mcts_player:
        return selection(currentNode, move_map, True)
    else:
        return random.choice(list(move_map.values()))

        

def main():
    chessboard = chess.Board()
    player = True
    portable_game_notation = []
    export = chess.pgn.Game()
    moves = 0
    while chessboard.is_game_over() == False:
        start_node = node()
        start_node.state = chessboard
        if player:
            print(portable_game_notation)
            print(chessboard)
        turn = mcts(start_node, player)
        chessboard.push_san(turn)
        moves += 1
        print(moves)
        portable_game_notation.append(turn)
        player = not player

    print(portable_game_notation)
    export.headers['Result'] = chessboard.result()



if __name__ == "__main__":
    main()
