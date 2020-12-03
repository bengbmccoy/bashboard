'''
A simple script to start aggregating the positions data for teams

'''

import pandas as pd
import numpy as np

def main():

    pbp_data = get_data('../data/reg_pbp.csv')
    # pbp_data = get_data('../data/sample_pbp.csv')
    pos_data = get_data('../data/pos_data.csv')

    pos_data.set_index(['season', 'gsis_id'], inplace=True)

    qb_cols = ['year', 'team', 'gained_air', 'gained_after_catch', 'gained_run', 'lost_air', 'lost_after_catch', 'lost_run']
    qb_table = pd.DataFrame(columns=qb_cols)
    qb_table.set_index(['team', 'year'], inplace=True)

    rb_cols = ['year', 'team', 'gained_run', 'gained_air', 'gained_after_catch', 'lost_run', 'lost_air', 'lost_after_catch']
    rb_table = pd.DataFrame(columns=rb_cols)
    rb_table.set_index(['team', 'year'], inplace=True)

    wr_cols = ['year', 'team', 'gained_air', 'gained_after_catch', 'lost_air', 'lost_after_catch']
    wr_table = pd.DataFrame(columns=wr_cols)
    wr_table.set_index(['team', 'year'], inplace=True)

    te_cols = ['year', 'team', 'gained_air', 'gained_after_catch', 'lost_air', 'lost_after_catch']
    te_table = pd.DataFrame(columns=te_cols)
    te_table.set_index(['team', 'year'], inplace=True)

    nan_list = []

    count = 0

    for index, row in pbp_data.iterrows():
        # Pass play
        # TODO: add yards conceded
        # TODO: need to add RB pass plays to rb_table
        # TODO: need to add WR and TE plays and tables

        count += 1
        if count % 1000 == 0:
            print(count)

        # print(row.play_id, row.game_id, row.play_type, row.receiver_player_id)

        if row.play_type == 'pass' and row.complete_pass == 1:
            year = row.game_date[:4]
            passer = row.passer_player_id
            catcher = row.receiver_player_id
            passer_pos, nan_list = get_pos(pos_data, passer, year, nan_list)
            catcher_pos, nan_list = get_pos(pos_data, catcher, year, nan_list)

            if passer_pos == 'QB':
                qb_table.fillna(0, inplace=True)

                try:
                    qb_table.at[(row.posteam, year), 'gained_air'] = row.air_yards + qb_table.at[(row.posteam, year), 'gained_air']
                    qb_table.at[(row.posteam, year), 'gained_after_catch'] = row.yards_after_catch + qb_table.at[(row.posteam, year), 'gained_after_catch']

                    qb_table.at[(row.defteam, year), 'lost_air'] = row.air_yards + qb_table.at[(row.defteam, year), 'lost_air']
                    qb_table.at[(row.defteam, year), 'lost_after_catch'] = row.yards_after_catch + qb_table.at[(row.defteam, year), 'lost_after_catch']
                except:
                    qb_table.at[(row.posteam, year), 'gained_air'] = row.air_yards
                    qb_table.at[(row.posteam, year), 'gained_after_catch'] = row.yards_after_catch

                    qb_table.at[(row.defteam, year), 'lost_air'] = row.air_yards
                    qb_table.at[(row.defteam, year), 'lost_after_catch'] = row.yards_after_catch

            # print(passer, catcher_pos, row.play_id, row.game_id)
            if catcher_pos == 'RB':
                rb_table.fillna(0, inplace=True)

                try:
                    rb_table.at[(row.posteam, year), 'gained_air'] = row.air_yards + rb_table.at[(row.posteam, year), 'gained_air']
                    rb_table.at[(row.posteam, year), 'gained_after_catch'] = row.yards_after_catch + rb_table.at[(row.posteam, year), 'gained_after_catch']

                    rb_table.at[(row.defteam, year), 'lost_air'] = row.air_yards + rb_table.at[(row.defteam, year), 'lost_air']
                    rb_table.at[(row.defteam, year), 'lost_after_catch'] = row.yards_after_catch + rb_table.at[(row.defteam, year), 'lost_after_catch']
                except:
                    rb_table.at[(row.posteam, year), 'gained_air'] = row.air_yards
                    rb_table.at[(row.posteam, year), 'gained_after_catch'] = row.yards_after_catch

                    rb_table.at[(row.defteam, year), 'lost_air'] = row.air_yards
                    rb_table.at[(row.defteam, year), 'lost_after_catch'] = row.yards_after_catch

            elif catcher_pos == 'WR':
                wr_table.fillna(0, inplace=True)

                try:
                    wr_table.at[(row.posteam, year), 'gained_air'] = row.air_yards + wr_table.at[(row.posteam, year), 'gained_air']
                    wr_table.at[(row.posteam, year), 'gained_after_catch'] = row.yards_after_catch + wr_table.at[(row.posteam, year), 'gained_after_catch']

                    wr_table.at[(row.defteam, year), 'lost_air'] = row.air_yards + wr_table.at[(row.defteam, year), 'lost_air']
                    wr_table.at[(row.defteam, year), 'lost_after_catch'] = row.yards_after_catch + wr_table.at[(row.defteam, year), 'lost_after_catch']
                except:
                    wr_table.at[(row.posteam, year), 'gained_air'] = row.air_yards
                    wr_table.at[(row.posteam, year), 'gained_after_catch'] = row.yards_after_catch

                    wr_table.at[(row.defteam, year), 'lost_air'] = row.air_yards
                    wr_table.at[(row.defteam, year), 'lost_after_catch'] = row.yards_after_catch

            elif catcher_pos == 'TE':
                te_table.fillna(0, inplace=True)

                try:
                    te_table.at[(row.posteam, year), 'gained_air'] = row.air_yards + te_table.at[(row.posteam, year), 'gained_air']
                    te_table.at[(row.posteam, year), 'gained_after_catch'] = row.yards_after_catch + te_table.at[(row.posteam, year), 'gained_after_catch']

                    te_table.at[(row.defteam, year), 'lost_air'] = row.air_yards + te_table.at[(row.defteam, year), 'lost_air']
                    te_table.at[(row.defteam, year), 'lost_after_catch'] = row.yards_after_catch + te_table.at[(row.defteam, year), 'lost_after_catch']
                except:
                    te_table.at[(row.posteam, year), 'gained_air'] = row.air_yards
                    te_table.at[(row.posteam, year), 'gained_after_catch'] = row.yards_after_catch

                    te_table.at[(row.defteam, year), 'lost_air'] = row.air_yards
                    te_table.at[(row.defteam, year), 'lost_after_catch'] = row.yards_after_catch


        # Run play
        # TODO: add QB runs to qb_table
        if row.play_type == 'run':

            rb_table.fillna(0, inplace=True)
            year = row.game_date[:4]
            runner = row.rusher_player_id
            runner_pos, nan_list = get_pos(pos_data, runner, year, nan_list)

            if runner_pos == 'QB':
                qb_table.fillna(0, inplace=True)

                try:
                    qb_table.at[(row.posteam, year), 'gained_run'] = row.yards_gained + qb_table.at[(row.posteam, year), 'gained_run']
                    qb_table.at[(row.defteam, year), 'lost_run'] = row.yards_gained + qb_table.at[(row.defteam, year), 'lost_run']
                except:
                    qb_table.at[(row.posteam, year), 'gained_run'] = row.yards_gained
                    qb_table.at[(row.defteam, year), 'lost_run'] = row.yards_gained

            elif runner_pos == 'RB':
                rb_table.fillna(0, inplace=True)

                try:
                    rb_table.at[(row.posteam, year), 'gained_run'] = row.yards_gained + rb_table.at[(row.posteam, year), 'gained_run']
                    rb_table.at[(row.defteam, year), 'lost_run'] = row.yards_gained + rb_table.at[(row.defteam, year), 'lost_run']
                except:
                    rb_table.at[(row.posteam, year), 'gained_run'] = row.yards_gained
                    rb_table.at[(row.defteam, year), 'lost_run'] = row.yards_gained

    print(qb_table)
    print(rb_table)
    print(wr_table)
    print(te_table)
    print(len(nan_list))

    qb_table.reset_index(inplace=True)
    save_csv(qb_table, '../data/qb_yards.csv')
    rb_table.reset_index(inplace=True)
    save_csv(rb_table, '../data/rb_yards.csv')
    wr_table.reset_index(inplace=True)
    save_csv(wr_table, '../data/wr_yards.csv')
    te_table.reset_index(inplace=True)
    save_csv(te_table, '../data/te_yards.csv')

def get_pos(pos_data, player, year, nan_list):
    '''This function takes the pos_data DF, a player id and a year and
    returns the position of that player or NaN if the player is not in the DB
    '''

    try:
        pos = pos_data.at[(int(year), player), 'position']
    except:
        pos = np.nan
        if player not in nan_list:
            nan_list.append(player)
            # print(player, year)
    return pos, nan_list

def get_data(filename):
    return pd.read_csv(filename)

def save_csv(df, file_name):
    df.to_csv(file_name, index=False)

if __name__ == "__main__":
    main()
