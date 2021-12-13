import chess
import host_chess_game
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from tqdm import tqdm
from os import listdir

INITIAL_ELO = 1200
K = 32 # for weaker players, 16 for masters

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
    #make_plot(50)






if __name__ == "__main__":
    main()
