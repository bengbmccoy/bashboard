'''
Thus script takes offence/defence and a team and a year as arguments.
It then access the reg_pbp.csv file and produces a 3x3 square plot showing
the yards gained above/below avg for each of:
play_type (run, short pass, long pass)
direction (left, middle, right)
'''

# Libraries
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import argparse

def main():

    # Command line arguments for team and bin_size
    parser = argparse.ArgumentParser()
    parser.add_argument('-off_def', type=str, default='off',
                        help='Plot the offence or the defence: "off" or "def"')
    parser.add_argument('-team', type=str, default='SEA',
                        help='the team you want to analyse the off/def of')
    parser.add_argument('-year', nargs='+', type=int, default=[2019],
                        help='the year that you want to analyse, only 2019 atm')
    parser.add_argument('-s', '--save', help='save the plot in charts',
                        action='store_true')
    parser.add_argument('-p', '--plot', help='plots the heatmap',
                        action='store_true')
    args = parser.parse_args()

    # Parse args
    team = args.team
    off_def = args.off_def
    year = args.year

    data = get_data(off_def, year)
    # print(data)

    plot_array, labels_array = init_arrays()
    # print(plot_array, labels_array)

    plot_array, labels_array = process_arrays(data, plot_array, labels_array, team)
    # print(plot_array, labels_array)

    if args.plot or args.save:
        generate_plot(plot_array, labels_array, off_def, team, year, args.save, args.plot)

def generate_plot(plot_array, labels_array, off_def, team, year, save, plot):
    '''Generates the heatmap plots, where the colormap is based on league
    rankings but the label is th diff vs league avg of that playtype and
    direction combination'''

    # resize labels array to be per match
    labels_array = labels_array/16

    # prepare title, axes labels and colors
    if off_def == 'off':
        color = 'Greens'
        title = '''A heatmap showing avg yards per game gained above/below
                    league average for each play type and play direction'''
    else:
        color = 'Reds'
        title = '''A heatmap showing avg yards per game conceded above/below
                    league average for each play type and play direction '''
    title += 'for ' + str(team) + ' during the ' + str(year) + ' seasons'
    xticklabels = ['left', 'middle', 'right']
    yticklabels = ['long pass', 'short pass', 'run']

    # start the plot
    fig, ax = plt.subplots()
    ax = sns.heatmap(plot_array, annot=labels_array, fmt = '', vmin=1, vmax=32,
                    cmap=color)
    ax.set_yticklabels(yticklabels, rotation = 0)
    ax.set_xticklabels(xticklabels, rotation = 0)
    ax.set_title(title)

    if save:

        fname = '../charts/heatmap_3x3_' + str(off_def)
        plt.savefig(fname)

    if plot:
        plt.show()


def process_arrays(data, plot_array, labels_array, team):
    '''Fill the plot_array and labels_array arrays by iterating through runs
    short passes and long passes and finding the rank and comparisson to the
    league average.'''

    # Set index to Team
    data.set_index('Team', inplace=True)
    # print(data)

    # Iterate through matrix rows
    for i in range(3):
        # Iterate through matrix cols
        for j in range(3):

            # generate column name to reference in data
            col_name = ''
            if i == 2:
                col_name += 'Run '
            elif i == 1:
                col_name += 'Pass short '
            elif i == 0:
                col_name += 'Pass long '

            if j == 0:
                col_name += 'left'
            elif j == 1:
                col_name += 'middle'
            elif j == 2:
                col_name += 'right'

            # sort by col_name
            data.sort_values(by=col_name, inplace=True)
            # get index of team after sorted
            plot_array[i,j] = data.index.get_loc(team)
            # find league avg of col_name
            avg = data[col_name].mean()
            # get diff vs league avg of col_name
            labels_array[i,j] = data.at[team, col_name] - avg

    # return arrays
    return plot_array, labels_array


def init_arrays():
    '''Return two empty arrays of dimensions 3x3 to be used for plot colour
    mapping and label values'''

    plot_array = np.empty([3,3])
    labels_array = np.empty([3,3])

    return plot_array, labels_array

def get_data(off_def, year):
    '''Get the aggregate offensive/defensive CSVs depending on off_def value,
    then aggregate based on the year and finally return dataframe'''

    if off_def == 'off':
        data = pd.read_csv('../data/agg_yards_off.csv')
    elif off_def == 'def':
        data = pd.read_csv('../data/agg_yards_def.csv')

    # TODO: be able to aggregate multiple years
    return data.loc[data['Year'].isin(year)]



if __name__ == "__main__":
    main()
