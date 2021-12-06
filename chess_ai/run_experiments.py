import chess
import host_chess_game
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from tqdm import tqdm

INITIAL_ELO = 1200
K = 32 # for weaker players, 16 for masters

def simulate_many_games(white, black, num_games=10):
    elo_W = [INITIAL_ELO]
    elo_B = [INITIAL_ELO]
    for game_num in tqdm(range(num_games)):
        exp_result_W = 1./(1+10**((elo_B[-1] - elo_W[-1])/400.))
        exp_result_B = 1./(1+10**((elo_W[-1] - elo_B[-1])/400.))
        result = host_chess_game.host_game(white=white, black=black, print_updates=False, print_output=False)
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
    print(elo_W[-1])
    print(elo_B[-1])

    fig  = plt.figure()
    plt.plot(np.arange(num_games+1), elo_W, label="absearch2_W")
    plt.plot(np.arange(num_games+1), elo_B, label="absearch3_B")
    plt.xlabel("Game Number")
    plt.ylabel("Elo Score")
    plt.legend()

    plt.show()
    fig.savefig("elo_scores.png", bbox_inches = 'tight', facecolor="white")



def main():
    start = datetime.now()
    simulate_many_games("alpha_beta_ai", "alpha_beta_ai", num_games=50)
    end = datetime.now()
    print("Total time:", end-start)



if __name__ == "__main__":
    main()
