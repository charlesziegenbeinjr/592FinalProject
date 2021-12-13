import chess
import host_chess_game
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from tqdm import tqdm
from os import listdir

INITIAL_ELO = 1200
K = 32 # for weaker players, 16 for masters


'''
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
'''
def simulate_many_games(white, black, kriegspiel=False, num_games=10, num_runs=10):
    total_runs_W = []
    total_runs_B = []
    for run_num in range(num_runs):
        elo_W = [INITIAL_ELO]
        elo_B = [INITIAL_ELO]
        for game_num in tqdm(range(num_games)):
            exp_result_W = 1./(1+10**((elo_B[-1] - elo_W[-1])/400.))
            exp_result_B = 1./(1+10**((elo_W[-1] - elo_B[-1])/400.))
            result = host_chess_game.host_game(white=white, black=black, kriegspiel=kriegspiel, print_updates=False, print_output=False)
            if result == "1-0":
                s_w = 1
                s_b = 0
            elif result == "0-1":
                s_w = 0
                s_b = 1
            else:
                s_w = 0.5
                s_b = 0.5
            elo_W.append(elo_W[-1] + K * (s_w - exp_result_W))
            elo_B.append(elo_B[-1] + K * (s_b - exp_result_B))
        total_runs_W.append(elo_W)
        total_runs_B.append(elo_B)
        rng = np.random.default_rng()
        np.savez("results" + str(rng.integers(10000000)) + ".npz", elo_W=np.array(elo_W), elo_B=np.array(elo_B))
    total_runs_W = np.array(total_runs_W)
    total_runs_B = np.array(total_runs_B)

    make_plot(num_games)

    # avg_per_game_W = np.average(total_runs_W, axis=0)
    # avg_per_game_B = np.average(total_runs_B, axis=0)
    # std_per_game_W = np.std(total_runs_W, axis=0)
    # std_per_game_B = np.std(total_runs_W, axis=0)
    #
    # colors = ["tab:blue", "tab:orange", "tab:green"]
    # light_colors = ["lightblue", "peachpuff", "honeydew"]
    #
    # fig  = plt.figure()
    # plt.plot(np.arange(num_games+1), avg_per_game_W, label="absearch_W", c=colors[0])
    # plt.plot(np.arange(num_games+1), avg_per_game_B, label="random_B", c=colors[1])
    # plt.fill_between(np.arange(num_games+1), avg_per_game_W, avg_per_game_W+std_per_game_W, where=avg_per_game_W+std_per_game_W>=avg_per_game_W,facecolor=light_colors[0])
    # plt.fill_between(np.arange(num_games+1), avg_per_game_W, avg_per_game_W-std_per_game_W, where=avg_per_game_W-std_per_game_W<=avg_per_game_W, facecolor=light_colors[0])
    # plt.fill_between(np.arange(num_games+1), avg_per_game_B, avg_per_game_B+std_per_game_B, where=avg_per_game_B+std_per_game_B>=avg_per_game_B,facecolor=light_colors[1])
    # plt.fill_between(np.arange(num_games+1), avg_per_game_B, avg_per_game_B-std_per_game_B, where=avg_per_game_B-std_per_game_B<=avg_per_game_B, facecolor=light_colors[1])
    # plt.xlabel("Game Number")
    # plt.ylabel("Average Elo Score")
    # plt.legend()
    #
    # plt.show()
    # fig.savefig("elo_scores.png", bbox_inches = 'tight', facecolor="white")

'''
 make_plot:

This function calls upon functionality to create plots that show the average ELO scores for the 15 runs, 100 games per run.
Similar to HW4 in setup as for the plotting.

Parameters:
    - num_games - the number of games to plot for

Returns:
    A plot showing the average elo scores for each game, with the number of elo scores being average for a specific game as the
    number of runs passed in
'''
def make_plot(num_games):
    total_runs_W = []
    total_runs_B = []
    for filename in listdir("."):
        if filename[-1] == "z":
            data = np.load(filename)
            total_runs_W.append(data["elo_W"])
            total_runs_B.append(data["elo_B"])
    total_runs_W = np.array(total_runs_W)
    total_runs_B = np.array(total_runs_B)

    avg_per_game_W = np.average(total_runs_W, axis=0)
    avg_per_game_B = np.average(total_runs_B, axis=0)
    std_per_game_W = np.std(total_runs_W, axis=0)
    std_per_game_B = np.std(total_runs_W, axis=0)

    colors = ["tab:blue", "tab:orange", "tab:green"]
    light_colors = ["lightblue", "peachpuff", "honeydew"]

    fig  = plt.figure()
    plt.plot(np.arange(num_games+1), avg_per_game_W, label="alpha_beta_W_depth_3", c=colors[0])
    plt.plot(np.arange(num_games+1), avg_per_game_B, label="alpha_beta_B_depth_2", c=colors[1])
    plt.fill_between(np.arange(num_games+1), avg_per_game_W, avg_per_game_W+std_per_game_W, where=avg_per_game_W+std_per_game_W>=avg_per_game_W,facecolor=light_colors[0])
    plt.fill_between(np.arange(num_games+1), avg_per_game_W, avg_per_game_W-std_per_game_W, where=avg_per_game_W-std_per_game_W<=avg_per_game_W, facecolor=light_colors[0])
    plt.fill_between(np.arange(num_games+1), avg_per_game_B, avg_per_game_B+std_per_game_B, where=avg_per_game_B+std_per_game_B>=avg_per_game_B,facecolor=light_colors[1])
    plt.fill_between(np.arange(num_games+1), avg_per_game_B, avg_per_game_B-std_per_game_B, where=avg_per_game_B-std_per_game_B<=avg_per_game_B, facecolor=light_colors[1])
    plt.xlabel("Game Number")
    plt.ylabel("Average Elo Score")
    plt.legend()

    plt.show()
    fig.savefig("elo_scores.png", bbox_inches = 'tight', facecolor="white")



def main():
    start = datetime.now()
    simulate_many_games("alpha_beta_ai", "alpha_beta_ai",
                        kriegspiel=False, num_games=100, num_runs=15)
    end = datetime.now()
    print("Total time:", end-start)






if __name__ == "__main__":
    main()
