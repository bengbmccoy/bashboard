# Libraries
import matplotlib.pyplot as plt
import pandas as pd
from math import pi
import argparse

def main():

    # Command line arguments for team and bin_size
    parser = argparse.ArgumentParser()
    parser.add_argument('-offence', type=str, default='SEA',
                        help='the team you want to analyse the offence of')
    parser.add_argument('-defence', type=str, default='None',
                        help='the team you want to analyse the defence of')
    parser.add_argument('-year', nargs='+', type=int, default=[2019],
                        help='the year that you want to analyse')
    parser.add_argument('-avg', action='store_true',
                        help='would you like to display the average offence')
    args = parser.parse_args()

    # define team and bin_size
    OFF = args.offence
    DEF = args.defence
    YEAR = args.year
    NUM_GAMES = len(YEAR) * 16

    # Set data
    if OFF != 'None':
        off_df = get_data('../data/agg_yards_off.csv')
        off_df = off_df.loc[(off_df['Team'] == OFF) & (off_df['Year'].isin(YEAR))]
        off_df.drop(['Year', 'Team'], axis=1, inplace=True)
        off_values = off_df.sum().tolist()
        off_values += off_values[:1]
        off_values[:] = [x / NUM_GAMES for x in off_values]
        # print(off_df)

    if DEF != 'None':
        def_df = get_data('../data/agg_yards_def.csv')
        def_df = def_df.loc[(def_df['Team'] == DEF) & (def_df['Year'].isin(YEAR))]
        def_df.drop(['Year', 'Team'], axis=1, inplace=True)
        def_values = def_df.sum().tolist()
        def_values += def_values[:1]
        def_values[:] = [x / NUM_GAMES for x in def_values]
        # print(def_df)

    if args.avg == True:
        avg_df = get_data('../data/agg_yards_off.csv')
        avg_df = avg_df.loc[(avg_df['Year'].isin(YEAR))]
        avg_df.drop(['Year', 'Team'], axis=1, inplace=True)
        avg_vals = avg_df.mean().to_list()
        avg_vals += avg_vals[:1]
        avg_vals[:] = [x / NUM_GAMES for x in avg_vals]
        print(avg_vals)

    # number of variables
    if OFF != 'None':
        categories=list(off_df)
    else:
        categories=list(def_df)
    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    # print(angles)

    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)
    # plt.show()

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='grey', size=8)
    # plt.show()

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([30,60,90], ["30","60","90"], color="grey", size=7)
    plt.ylim(0,90)
    # plt.show()

    # Plot data
    if OFF != 'None':
        ax.plot(angles, off_values, linewidth=1, linestyle='solid', color='g', label=str(OFF) + ' avg yards gained per game ' + str(YEAR))
        ax.fill(angles, off_values, 'g', alpha=0.1)
    if DEF != 'None':
        ax.plot(angles, def_values, linewidth=1, linestyle='solid', color='r', label=str(DEF) + ' avg yards conceded per game ' + str(YEAR))
        ax.fill(angles, def_values, 'r', alpha=0.1)
    if args.avg == True:
        ax.plot(angles, avg_vals, linewidth=1, linestyle='solid', color='b', label='League avg yards gained/conceded per game')
        ax.fill(angles, avg_vals, 'b', alpha=0.1)
    # plt.show()

    if DEF == 'None':
        plt.title('Average yards gained per game by play type during regular season')
    else:
        plt.title('Average yards gained/conceded per game \n by play type during regular season')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=3, fontsize = 6)
    plt.show()

def get_data(filename):
    return pd.read_csv(filename)

if __name__ == "__main__":
    main()
