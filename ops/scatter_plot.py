# Libraries
import matplotlib.pyplot as plt
import pandas as pd
from math import pi
import argparse

import seaborn as sns

def main():

    # Command line arguments for team and bin_size
    parser = argparse.ArgumentParser()
    parser.add_argument('-team', nargs='+', default=['SEA'],
                        help='the team you want to analyse the offence of')
    parser.add_argument('-year', nargs='+', type=int, default=[2019],
                        help='the year(s) that you want to analyse')
    parser.add_argument('-plot', action='store_true', default=False,
                        help='plot the scatter graph, default is False')
    parser.add_argument('-save_all', action='store_true', default=False,
                        help='save the aggregated data, default is False')
    args = parser.parse_args()

    TEAM = args.team
    YEAR = args.year

    df = get_data('../data/game_data.csv')
    df = df.loc[df['season'].isin(YEAR)]
    # print(df)

    cols = ['GameID', 'Points scored', 'Points conceded', 'Opponent', 'Location', 'Year', 'Week']
    agg_data = pd.DataFrame(columns=cols)

    if args.save_all == 'True':
        TEAM = set(df['home_team'].tolist())

    cols = ['GameID', 'Team', 'Opponent', 'Points scored', 'Points conceded', 'Location', 'Year', 'Week']
    agg_data = pd.DataFrame(columns=cols)

    for i in TEAM:

        print(i)

        for index, row in df.iterrows():
            data_dict = {}
            if row.home_team == i:
                data_dict['GameID'] = row.game_id
                data_dict['Team'] = i
                data_dict['Opponent'] = row.away_team
                data_dict['Points scored'] = row.home_score
                data_dict['Points conceded'] = row.away_score
                data_dict['Location'] = 'HOME'
                data_dict['Year'] = row.season
                data_dict['Week'] = row.week
                agg_data = agg_data.append(data_dict, ignore_index=True)
            if row.away_team == i:
                data_dict['GameID'] = row.game_id
                data_dict['Team'] = i
                data_dict['Opponent'] = row.home_team
                data_dict['Points scored'] = row.away_score
                data_dict['Points conceded'] = row.home_score
                data_dict['Location'] = 'AWAY'
                data_dict['Year'] = row.season
                data_dict['Week'] = row.week
                agg_data = agg_data.append(data_dict, ignore_index=True)

        if args.plot == True:
            x = agg_data['Points scored'].tolist()
            y = agg_data['Points conceded'].tolist()
            plt.scatter(x, y, label=i)

    # print(agg_data)

    if args.plot == True:
        plt.xlim(-1, 50)
        plt.ylim(-1, 50)
        plt.xlabel('Points scored')
        plt.ylabel('Points conceded')
        plt.title('A scatter point of points scored vs points conceeded for each match')
        plt.legend()
        plt.show()

    if args.save_all == True:
        save_csv(agg_data, '../data/agg_games.csv')

def save_csv(df, file_name):
    df.to_csv(file_name, index=False)

def get_data(filename):
    return pd.read_csv(filename)

if __name__ == "__main__":
    main()
