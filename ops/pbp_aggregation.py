'''
Written by Ben McCoy, Nov 2020

A script that takes the regular season play-by-play data stored in reg_pbp.csv
and aggregates the data into season long totals of yards gained/conceded by
play type.

The aggregated data is saved into a csv called 'agg_yards_off.csv' or
'agg_yards_def.csv'.

The output of this script is used for the radar_plot script to make radar plots
of the yards gained/conceded by different teams throughout different seasons.
'''

# import libraries
import pandas as pd
import numpy as np
import argparse

def main():

    # command line arguments for year and yards gained or conceeded
    parser = argparse.ArgumentParser()
    parser.add_argument('-year', nargs='+', type=int, default=[2017, 2018, 2019],
                        help='the year(s) that you want to aggregate, default is 2017, 2018 & 2019')
    parser.add_argument('-off_def', type=str, default='off',
                        help='aggregate offence (off) or defence (def), default is offence')
    parser.add_argument('-quiet', default=False, action='store_true',
                        help='stop showing print statements, defualt is False')
    args = parser.parse_args()

    years = args.year

    # collect the data
    data = get_data('../data/reg_pbp.csv')
    # print(data)

    # get list of all teams in pbp data
    all_teams = set(data['posteam'].tolist())
    all_teams.remove(np.nan)
    # print(all_teams)

    # all of the fields we want to aggregate the data into, and the initialisation
    # of the DF used to aggregate the results
    cols = ['Team', 'Year', 'Run right', 'Run middle', 'Run left', 'Pass short right',
            'Pass short middle', 'Pass short left', 'Pass long right', 'Pass long middle',
            'Pass long left']
    results = pd.DataFrame(columns=cols)

    # iterate through the years selected
    for year in years:

        # iterate through all of the teams
        for myteam in all_teams:

            # get a subset of the DF with only the current team for efficiency
            if args.off_def == 'off':
                myteam_data = data.loc[data['posteam'] == myteam]
            elif args.off_def == 'def':
                myteam_data = data.loc[data['defteam'] == myteam]
            # print(myteam_data)

            # init the data_dict used to calculate and append the aggregated values
            data_dict = {}

            data_dict['Team'] = myteam
            data_dict['Year'] = year

            data_dict['Pass short middle'] = 0
            data_dict['Pass short left'] = 0
            data_dict['Pass short right'] = 0

            data_dict['Pass long middle'] = 0
            data_dict['Pass long left'] = 0
            data_dict['Pass long right'] = 0

            data_dict['Run middle'] = 0
            data_dict['Run left'] = 0
            data_dict['Run right'] = 0

            # iterate through the rows in the DF and update the data_dict
            for index, row in myteam_data.iterrows():

                # make sure that it is the correct year
                if str(year) in row.game_date:

                    # store run play yards
                    if row.play_type == 'run':
                        if row.run_location == 'middle':
                            data_dict['Run middle'] = data_dict['Run middle'] + row.yards_gained
                        elif row.run_location == 'left':
                            data_dict['Run left'] = data_dict['Run left'] + row.yards_gained
                        elif row.run_location == 'right':
                            data_dict['Run right'] = data_dict['Run right'] + row.yards_gained

                    # store pass play yards
                    if row.play_type == 'pass':

                        # store short passing yards
                        if row.pass_length == 'short':
                            if row.pass_location == 'right':
                                data_dict['Pass short right'] = data_dict['Pass short right'] + row.yards_gained
                            elif row.pass_location == 'left':
                                data_dict['Pass short left'] = data_dict['Pass short left'] + row.yards_gained
                            elif row.pass_location == 'middle':
                                data_dict['Pass short middle'] = data_dict['Pass short middle'] + row.yards_gained

                        # store deep passing yards
                        elif row.pass_length == 'deep':
                            if row.pass_location == 'right':
                                data_dict['Pass long right'] = data_dict['Pass long right'] + row.yards_gained
                            elif row.pass_location == 'left':
                                data_dict['Pass long left'] = data_dict['Pass long left'] + row.yards_gained
                            elif row.pass_location == 'middle':
                                data_dict['Pass long middle'] = data_dict['Pass long middle'] + row.yards_gained

            # append the aggregated data into the results DF
            results = results.append(data_dict, ignore_index=True)

            if args.quiet == False:
                print(data_dict)

    # save the results csv
    if args.off_def == 'off':
        save_csv(results, '../data/agg_yards_off.csv')
    elif args.off_def == 'def':
        save_csv(results, '../data/agg_yards_def.csv')


def save_csv(df, file_name):
    df.to_csv(file_name, index=False)

def get_data(filename):
    return pd.read_csv(filename)

if __name__ == "__main__":
    main()
