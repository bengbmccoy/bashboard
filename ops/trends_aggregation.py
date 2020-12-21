'''
Written By: Ben McCoy Dec 2020

This code aggregates the play-by-play data into a concatenated csv whcih can be
indexed by team, and then displays the weekly play_type and play_direction yards_gained
and other meta data.

This data is to be used on the nfl dash board, for the yards gained by play_type
and play type usage.

To run:

$ python trends_aggregation.py

TODO:
- Add the filename as input from an argument
- Figure out a strategy for dealing with different seasons
'''

import pandas as pd
import numpy as np
from math import isnan

def main():

    # get the pbp data
    pbp_data = get_data('../data/reg_pbp.csv')
    # pbp_data = get_data('../data/sample_pbp.csv') # For debugging

    # Get list of teams & remove the nan
    teams = list(set(pbp_data['posteam'].to_list()))
    teams = [x for x in teams if str(x) != 'nan']

    # columns in the save_file csv
    columns = ['game_id', 'game_no', 'opp', 'play_type', 'play_direction', 'yards_gained']
    # play_type = ['game_id', 'opp', 'run_left', 'run_mid', 'run_right', 'short_pass_left', 'short_pass_mid', 'short_pass_right', 'long_pass_left', 'long_pass_mid', 'long_pass_right']

    # get list 1-16
    game_no = list(range(1, 17))

    # init the dataframe
    df1 = pd.DataFrame(columns=columns)

    # iterate through each game
    for h in game_no:
        # iterate through each play_type
        for i in ['run', 'short_pass', 'long_pass']:
            # iterate through each play_direction
            for j in ['left', 'middle', 'right']:
                # add a row
                df1 = df1.append({'game_id': np.nan, 'game_no': h, 'opp': np.nan, 'play_type': i, 'play_direction': j, 'yards_gained': 0}, ignore_index=True)

    # Used previously, cant remember what for
    # df1.fillna({'yards_gained': 0})
    # df1.fillna({'run_left': 0, 'run_mid': 0, 'run_right': 0, 'short_pass_left': 0, 'short_pass_mid': 0, 'short_pass_right': 0, 'long_pass_left': 0, 'long_pass_mid': 0, 'long_pass_right': 0}, inplace=True)

    # a dictionary to hold all the output dataframes
    df_dict = {}
    # a dictionary to keep track of game ids
    id_dict = {}

    # for each team, add the empty dataframe to the df_dict with the key as the
    # team and the value as the dataframe
    for i in teams:
        df_dict[i] = df1.copy()
        id_dict[i] = []
    # print(id_dict) # for debugging


    print(df_dict) # for debugging

    # old data model
    # save_file = process_data_old(pbp_data.copy(), teams, df_dict.copy(), id_dict.copy())

    # current data model
    save_file = process_data_new(pbp_data.copy(), teams, df_dict.copy(), id_dict.copy())

    # save the file
    save_csv(save_file, '../data/team_trends.csv')

    ''' DATA MODEL '''

def process_data_new(pbp_copy, teams, df_dict_copy, id_dict_copy):

    # iterate through every single play
    for index, row in pbp_copy.iterrows():

        # ensure that the game is from the 2019 season
        if row.game_date[:4] == '2019' or row.game_date[:4] == '2020':

            # print(row.game_id, row.home_team, row.away_team) # For debugging

            # if the game is not in the id_dict list, append it and add the game
            # to the next available game number and opp in the df_dict.
            if row.game_id not in id_dict_copy[row.home_team]:
                id_dict_copy[row.home_team].append(row.game_id)
                df_dict_copy[row.home_team].loc[(df_dict_copy[row.home_team].game_no) == len(id_dict_copy[row.home_team]), 'game_id'] = row.game_id
                df_dict_copy[row.home_team].loc[(df_dict_copy[row.home_team].game_no) == len(id_dict_copy[row.home_team]), 'opp'] = row.away_team
                print(row.home_team, df_dict_copy[row.home_team])

            # Same as above, except for away team
            if row.game_id not in id_dict_copy[row.away_team]:
                id_dict_copy[row.away_team].append(row.game_id)
                df_dict_copy[row.away_team].loc[(df_dict_copy[row.away_team].game_no) == len(id_dict_copy[row.away_team]), 'game_id'] = row.game_id
                df_dict_copy[row.away_team].loc[(df_dict_copy[row.away_team].game_no) == len(id_dict_copy[row.away_team]), 'opp'] = row.home_team
                print(row.away_team, df_dict_copy[row.away_team])

            # Add the run yards to the correct cell based on play_type, play_direction and game
            if row.play_type == 'run':
                df_dict_copy[row.posteam].loc[(df_dict_copy[row.posteam].game_id == row.game_id) & (df_dict_copy[row.posteam].play_type == row.play_type) & (df_dict_copy[row.posteam].play_direction == row.run_location), 'yards_gained'] += row.yards_gained

            # as above but with pass yards broken down by short or deep (20 yards)
            if row.play_type == 'pass':
                if row.pass_length == 'short':
                    df_dict_copy[row.posteam].loc[(df_dict_copy[row.posteam].game_id == row.game_id) & (df_dict_copy[row.posteam].play_type == 'short_pass') & (df_dict_copy[row.posteam].play_direction == row.pass_location), 'yards_gained'] += row.yards_gained
                if row.pass_length == 'deep':
                    df_dict_copy[row.posteam].loc[(df_dict_copy[row.posteam].game_id == row.game_id) & (df_dict_copy[row.posteam].play_type == 'long_pass') & (df_dict_copy[row.posteam].play_direction == row.pass_location), 'yards_gained'] += row.yards_gained

    # For debugging
    # for k, v in df_dict_copy.items():
    #     print(k, v)

    # Concat each dataframe int eh dict and return
    return (pd.concat(df_dict_copy.values(), keys=df_dict_copy.keys()))



def process_data_old(pbp_copy, teams, df_dict_copy, id_dict_copy):
    # print(id_dict_copy)
    for index, row in pbp_copy.iterrows():
        if row.game_date[:4] == '2019' or row.game_date[:4] == '2020':
            # pass
            # print(row.game_id, row.home_team, row.away_team)
            if row.game_id not in id_dict_copy[row.home_team]:
                id_dict_copy[row.home_team].append(row.game_id)
                df_dict_copy[row.home_team].at[len(id_dict_copy[row.home_team]), 'game_id'] = row.game_id
                df_dict_copy[row.home_team].at[len(id_dict_copy[row.home_team]), 'opp'] = row.away_team
                print(row.home_team, df_dict_copy[row.home_team])

            if row.game_id not in id_dict_copy[row.away_team]:
                id_dict_copy[row.away_team].append(row.game_id)
                df_dict_copy[row.away_team].at[len(id_dict_copy[row.away_team]), 'game_id'] = row.game_id
                df_dict_copy[row.away_team].at[len(id_dict_copy[row.away_team]), 'opp'] = row.home_team
                print(row.away_team, df_dict_copy[row.away_team])

            if row.play_type == 'run':
                if row.run_location == 'left':
                    df_dict_copy[row.posteam].at[len(id_dict_copy[row.posteam]), 'run_left'] += row.yards_gained
                if row.run_location == 'middle':
                    df_dict_copy[row.posteam].at[len(id_dict_copy[row.posteam]), 'run_mid'] += row.yards_gained
                if row.run_location == 'right':
                    df_dict_copy[row.posteam].at[len(id_dict_copy[row.posteam]), 'run_right'] += row.yards_gained

            if row.play_type == 'pass':
                if row.pass_length == 'short':
                    if row.pass_location == 'left':
                        df_dict_copy[row.posteam].at[len(id_dict_copy[row.posteam]), 'short_pass_left'] += row.yards_gained
                    if row.pass_location == 'middle':
                        df_dict_copy[row.posteam].at[len(id_dict_copy[row.posteam]), 'short_pass_mid'] += row.yards_gained
                    if row.pass_location == 'right':
                        df_dict_copy[row.posteam].at[len(id_dict_copy[row.posteam]), 'short_pass_right'] += row.yards_gained

                if row.pass_length == 'deep':
                    if row.pass_location == 'left':
                        df_dict_copy[row.posteam].at[len(id_dict_copy[row.posteam]), 'long_pass_left'] += row.yards_gained
                    if row.pass_location == 'middle':
                        df_dict_copy[row.posteam].at[len(id_dict_copy[row.posteam]), 'long_pass_mid'] += row.yards_gained
                    if row.pass_location == 'right':
                        df_dict_copy[row.posteam].at[len(id_dict_copy[row.posteam]), 'long_pass_right'] += row.yards_gained

    for k, v in df_dict_copy.items():
        print(k, v)

    return (pd.concat(df_dict_copy.values(), keys=df_dict_copy.keys()))



def get_data(filename):
    return pd.read_csv(filename)

def save_csv(df, file_name):
    print(df)
    df.to_csv(file_name, index=True)

if __name__ == "__main__":
    main()
