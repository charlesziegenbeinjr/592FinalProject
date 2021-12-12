How To Run Our Programs:

1. If you want to play a Games in a Non-Testing Suite:


Our repository is set up as follows:

Files:
- node.py
- host_chess_game.py
- run_experiments.py
- alpha_beta_ai.py
- mcts_ai.py
- heuristics.py
- utils.py


***********
* node.py *
***********

General Description:

    Supports the creation of a Node object, the objects that form
    the contents of the search trees that we iterate through in
    the MCTS and AB algorithms. Contains functions native to the 
    Node object.

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

        Functions:
            
            Node.__init__:

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

            Node.get_heuristic:

                Returns the value computed by the heuristic for both Kriegspiel and 
                Regular chess

                Parameters:
                    curr_player - the current player, W or B
                    update_v - Boolean, updates the win/loss of current node
                    when set to True

                Returns:
                    the heuristic value for the node

            Node.remove_opponent_pieces:

                For Kriegspiel, removes the opponents pieces from the legal_moves array when playing Kriegspiel

                Parameters:
                    curr_player - the current player, I.E whose turn it is when this function is called
                
                Returns:
                    Void return, instead removes pieces on the board_state of the node

            Node.get_diag_pawn_moves:

                For Kriegspiel, an edge case state when we need to get the number of diagonal pawn moves that can be made.
                Given the setup of Kriegspiel, not knowing where the opponent's pieces are can make python-chess think there aren't 
                legal moves remaining, so this checks to see if a pawn capture can be made, as diagonal pawn moves aren't legal unless
                it is a legal capture move

                Parameters:
                    curr_player - the current player, I.E whose turn it is when this function is called

                Returns:
                    Void return, instead adds potential diagonal pawn moves for capture to the diag_pawn_moves property of the current node

            Node.get_nth_best_move:

                !!! FILL IN !!!

                Parameters:
                    n - 
                    curr_player - the current player, I.E whose turn it is when this function is called
                
                Returns:


            Node.update_opponent_pieces

                !!! FILL IN !!!

                Parameters:
                    curr_player - the current player, I.E whose turn it is when this function is called
                    full_board_state - 

                Returns:



**********************
* host_chess_game.py *
**********************

General Description:

The driver script for running individual games of chess or Kriegspiel. Facilitates the user picking which players to play the game,
which can either be human, an AI type, or random. Prints updates after each move if requested and prints the outcome of the game.
Calculates the time that was taken to simulte the number of games requested

Global Variables:
- Depth: the depth to be taken in the search tree by the Alpha Beta AI in alpha_beta_ai.py
    - Associated depth for the White player W and Black player B

Funtions:
    
    setup_board:

        Takes in an initial setup, if there is any. If left blank, we create a new default chessboard to start
        the game from

        Parameters:
            - initial_setup: String, will be in FEN notation, which python-chess can interpret as an initial opponent_pieces

        Returns:
            a starting chessboard, either predefined by the user or as a starting board used in standard games


    host_game:

        Effectively hosts the game between two players. Drives the two players, calling their respective functions based on the type of 
        player that was selected to play. Switches the player and updates the board when the current players turn is over.
        Prints updates to the board itself following opponent moves and prints the final state of the board upon conclusion of the game

        Parameters:
            - initial_setup - String, the initial setup of the board that is requested: either standard or a board in FEN notation
            - white - String, the type of player that will be playing as white: can be "human", "mcts_ai", "alpha_beta_ai", or "random"
            - black - String, the type of player that will be playing as black: can be "human", "mcts_ai", "alpha_beta_ai", or "random"
            - kriegspiel - Boolean, whether or not we will be playing Kriegspiel (T) or standard Chess (F)
            - print_updates - Boolean, whether we should print updates after each move (T) or not (F)
            - print_output - Boolean, whether we should print the final game state (T) or not (F) following the end of the game

        Returns:
            IF there is an error with the type of player specified in the original function call, return "INVALID AI TYPE"
            ELSE returns the outcome of the game result, loops through until the end of the game. Once the end of the game is 
            prints the winning player, the outcome and returns the python-chess defined end game reason so for data purposes
        

        Returns:
            The outcome of the chess game, if there are no errors in the way that the function is specified (namely, if the AI type passed in
            is not defined)

    main:

        The driver of the script, calls host_game() in an amount specified by a loop parameter, effectively simulating multiple games by differnet
        types of AI specified by the end-user. Reports the amount of time taken

        Parameters:
            NO PARAMETERS
        
        Returns:
            Null, prints the time taken for a game simulation to run



**********************
* run_experiments.py *
**********************

General Description:

The driver script for the experiments suite. Also contains functionality to generate plots.

Global Variables:
- INITIAL_ELO: the initial elo score to be used for each player that will be playing in the simulations
- K: the K factor, a cap on how many Elo points a player can win or lose from a single match based on rating

Functions:
    
    simulate_many_games:

        This function calls upon host_chess_game functionality to simulate the chess games, and creates a loop that 
        will run the simulations a set number of times. For each game, it calculates the resulting ELO, 
        and appends it to a list of elo scores, helping an end user understand how the players are doing over time.
        Also calls upon the make plots function with the number of games so as to plot the changes in ELO scores over
        a set number of games

        Parameters:
            - white - String, the type of player that white is: random, an AI player, or human
            - black - String, the type of player that black is: random, an AI player, or human
            - kriegspiel - Boolean, whether the experiments are for kriegspiel or not
            - num_games - Int, the number of games per run to simulate
            - num_runs - Int, the number of runs to simulate in an experiment
        
        Returns:
            Null, effectively calculates the changes in ELO and then calls the make_plot function to generate a plot
            for the observed 

    make_plot:
        
        This function calls upon functionality to create plots that show the average ELO scores for the 15 runs, 100 games per run.
        Similar to HW4 in setup as for the plotting.

        Parameters:
            - num_games - the number of games to plot for
        
        Returns:
            A plot showing the average elo scores for each game, with the number of elo scores being average for a specific game as the
            number of runs passed in


*****************
* heuristics.py * 
*****************

General Description:

This file implements the chess heuristics that were used in both AB and MCTS chess.

Global Variables:
- PIECE_VALUES: defines the values of each piece in Chess

Functions:

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
    

    count_attacks:

        Counts the total number of pieces that can be attacked based on the setup of the board
        and the player whose turn it is

        Parameters:
            - board_state - python-chess BoardState, the current status of the chessboard
            - curr_player - String, the current player "W" or "B"
        
        Returns:
            The number of pieces that can be attacked based on the chessboard setup and the current player
            based on their remaining pieces
    

    opponent_check:

        




********************
* alpha_beta_ai.py * 
********************

General Description:

Script for running the Alpha Beta Search algorithm for either Chess or Kriegspiel.

Functions:

    depth_limited_ab_search:

        Similar to the textbook version, but Depth Limited Alpha Beta Search. 
        Recursively called to go down the depth that set in the function call.

        Parameters:
            - node - Node object, the current node
            - depth - int, the depth of the tree that is to be explored
            - alpha - float, the value of alpha, -infinity
            - beta - float, the value of beta, infinity
            - maximizing_player - Boolean, whether or not the current player is the maximizing player
            - curr_player - the current player, either B or W

        Returns:
            returns the optimal move selected by the A/B search algorithm



**************
* mcts_ai.py *
**************

General Description:

Script for running the MCTS algorithm for either Chess or Kriegspiel.

Functions:

    mcts:

        The driver for the MCTS algorithm. Gnerates the possible moves, and sets
        the number of simulations for the selection, expansion, playout and backprop
        functions. Calculates the final move to return

        Parameters:
            - currentNode - Node, the current node in question, generated by host_game
            - kriegspiel - Boolean, whether we are playing kriegspiel or not

        Returns:
            Returns the node that is selected by MCTS, the move that is played on the board
    
    selection:

        The selection algorithm. Iterate through all the child of the given state and select 
        the one with highest UCB value.

        Parameters:
            - currentNode - Node, the current node to select a child from
        
        Returns:
            The child of the current node with the highest UCB1 value
    
    UCB1:

        Expansion/Exploration function. currentNode.v + np.sqrt(2) *
        (np.sqrt(np.log(currentNode.N + np.exp(1) + (10**-7)) / (currentNode.n + (10**-11))))
        as defined by the book. Notice the terms to avoid DivisionByZero.

        Parameters:
            - currentNode: node, the node that has been passed to the UCB1 algorithm, is a child
            of the current node from selection
        
        Returns:
            The UCB1 value calculated by the formula for the child.

    expansion:

        Recursively keep on calling the 
        child with maximum UCB1 till we reach the end of the tree or number of simulations.

        Parameters:
            currentNode - Node, the current node in question to expand
            player - String, either the black or white player.

        Returns:
            The currentNode as selected by repeated calls to selection, either returned because end of 
            tree reached, or simulations ended

    playout:

        Upon getting a Node from expansion, playout will make moves based on heuristic function till we 
        reach end of the game and will return leaf node. 
        If we reach the end of the game, we evaluate the result of the game and send values back accordingly.

        Parameters:
            - currentNode - Node, playout from the current Node in question
            - depth - Int, experimental parameter for depth efficiency testing

        Returns:
            The currentNode that we ended with and the reward associated with reaching that node per the end game
            result.
    
    backpropagate:

        Receives the final node and reward from playout. Traverses that reward till the root of the tree which will
        in turn update the Node parameters N, n and v, that impact the UCB1 values of each node in the path.

        Parameters:
            - currentNode - Node, the current node in question
            - reward - Float, the reward associated with the currentNode being the leaf
        
        Returns:
            Returns the currentNode. 



************
* utils.py *
************

General Description:

General utility functions for getting the board state and pretty-printing out the board.

Functions:

    get_board_state_array:

        Get the state of the board in the form of an list

        Parameters:
            - board_state - python-chess's BoardState, the chessboard state
        
        Returns:
            Returns the board state in list form instead of a full-fledged chess notation


    pretty_print_board:

        Prints the chessboard in a pretty way

        Parameters:
            - board_state - python-chess's BoardState, the chessboard state
        
        Returns:
            Void return, prints out the board in the format defined by the function.