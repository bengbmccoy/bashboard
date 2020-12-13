'''
A simple script to start aggregating the positions data for teams

'''
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

class HeatmapPlot:
    def __init__(self, year, positions, plots):
        self.year = year
        self.positions = positions
        self.plot = plots
        self.qb_data = pd.DataFrame()
        self.rb_data = pd.DataFrame()
        self.wr_data = pd.DataFrame()
        self.te_data = pd.DataFrame()

    def get_data(self):
        year = self.year
        self.qb_data = get_data('../data/qb_yards.csv')
        self.rb_data = get_data('../data/rb_yards.csv')
        self.wr_data = get_data('../data/wr_yards.csv')
        self.te_data = get_data('../data/te_yards.csv')

        self.qb_data = self.qb_data.loc[self.qb_data['year'] == year]
        self.rb_data = self.rb_data.loc[self.rb_data['year'] == year]
        self.wr_data = self.wr_data.loc[self.wr_data['year'] == year]
        self.te_data = self.te_data.loc[self.te_data['year'] == year]

    def gen_plots(self):
        pass



def main():

    # Command line arguments for team and bin_size
    parser = argparse.ArgumentParser()
    parser.add_argument('-year', type=int, default=2019,
                        help='the year(s) that you want to analyse')
    parser.add_argument('-plot', action='store_true', default=False,
                        help='plot the scatter graph, default is False')
    # parser.add_argument('-save_all', action='store_true', default=False,
    #                     help='save the aggregated data, default is False')
    args = parser.parse_args()

    year = args.year
    positions = ['QB', 'RB']
    plots = ['run', 'air', 'catch']

    qb_data = get_data('../data/qb_yards.csv')
    rb_data = get_data('../data/rb_yards.csv')
    wr_data = get_data('../data/wr_yards.csv')
    te_data = get_data('../data/te_yards.csv')

    qb_data_2019 = qb_data.loc[qb_data['year'] == year]
    rb_data_2019 = rb_data.loc[rb_data['year'] == year]
    wr_data_2019 = wr_data.loc[wr_data['year'] == year]
    te_data_2019 = te_data.loc[te_data['year'] == year]

    for i in positions:
        for j in plots:
            heatmap_plot(i, j)

    '''

    rb_data_2019.set_index('team', inplace=True)
    print(rb_data_2019)

    teams = qb_data_2019.team.tolist()
    rb_data_2019.sort_values(by='gained_run', ascending=False, inplace=True)
    ascending_rb_gained_run = rb_data_2019.index.tolist()
    rb_data_2019.sort_values(by='lost_run', ascending=False, inplace=True)
    ascending_rb_lost_run = rb_data_2019.index.tolist()
    print(ascending_rb_gained_run)
    print(ascending_rb_lost_run)

    rb_run_matrix = pd.DataFrame(columns=ascending_rb_lost_run)
    print(rb_run_matrix)

    for i in ascending_rb_gained_run:
        result = {}
        for j in ascending_rb_lost_run:
            result[j] = (rb_data_2019.loc[i]['gained_run']/16 + rb_data_2019.loc[j]['lost_run']/16)/2
        rb_run_matrix.loc[i] = result
    print(rb_run_matrix)



    # heatmap
    sns.heatmap(rb_run_matrix, annot=True,fmt=".3g", annot_kws={"size": 7}, xticklabels=True, yticklabels=True, cmap='PuOr')
    # sns.heatmap(rb_run_matrix_norm, annot=True, annot_kws={"size": 7}, xticklabels=True, yticklabels=True, cmap='PuOr')

    '''

    if args.plot:
        plt.show()

def heatmap_plot(i, j):
    print(i, j)



def get_data(filename):
    return pd.read_csv(filename)

def save_csv(df, file_name):
    df.to_csv(file_name, index=False)


if __name__ == "__main__":
    main()
