'''
A simple script to start parsing and analysing the score data for teams

'''

import pandas as pd
import numpy as np
import random
from matplotlib import pyplot as plt
import argparse

def main():

    # Command line arguments for team and bin_size
    parser = argparse.ArgumentParser()
    parser.add_argument('-team', type=str, default='SEA',
                        help='the team you want to analyse the points of')
    parser.add_argument('-bin_size', type=int, default='3',
                        help='the number of bins you want, default is 3')
    args = parser.parse_args()

    # define team and bin_size
    team = args.team
    bin_size = args.bin_size

    # get the home and away data for the team and place in one df
    game_data = get_data('../data/game_data.csv')
    score_home_data = game_data.loc[game_data['home_team'] == team]
    score_away_data = game_data.loc[game_data['away_team'] == team]
    score_game_data = pd.concat([score_away_data, score_home_data])

    # For debugging
    print(score_game_data)

    # collect the points scored and points conceeded for your team in each game
    scored = []
    conceded = []
    for index, row in score_game_data.iterrows():
        if row.home_team == team:
            scored.append(row.home_score)
            conceded.append(row.away_score)
        if row.away_team == team:
            scored.append(row.away_score)
            conceded.append(row.home_score)

    # For debugging
    print(scored)
    print(conceded)

    # set up the bins
    bins = np.arange(0, 50, bin_size) # fixed bin size

    # histogram config
    plt.xlim(0, 50)
    plt.hist(scored, bins=bins, alpha=0.5, label='points scored', color='green')
    plt.hist(conceded, bins=bins, alpha=0.5, label='points conceeded', color='red')
    plt.title('Histogram of points scored vs points conceeded for ' + str(team) + ' in 2018 & 2019')
    plt.xlabel('Points (bin size = ' + str(bin_size) + ')')
    plt.ylabel('frequency')
    plt.legend()

    # plot the histogram
    plt.show()

def get_data(filename):
    return pd.read_csv(filename)

if __name__ == "__main__":
    main()
