'''
A simple script to start aggregating the positions data for teams

'''
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():


    qb_data = get_data('../data/qb_yards.csv')
    rb_data = get_data('../data/rb_yards.csv')
    wr_data = get_data('../data/wr_yards.csv')
    te_data = get_data('../data/te_yards.csv')

    qb_data_2019 = qb_data.loc[qb_data['year'] == 2019]
    rb_data_2019 = rb_data.loc[rb_data['year'] == 2019]
    wr_data_2019 = wr_data.loc[wr_data['year'] == 2019]
    te_data_2019 = te_data.loc[te_data['year'] == 2019]

    rb_data_2019.set_index('team', inplace=True)
    print(rb_data_2019)

    teams = qb_data_2019.team.tolist()
    print(teams)

    rb_run_matrix = pd.DataFrame(columns=teams)
    print(rb_run_matrix)

    for i in teams:
        result = {}
        for j in teams:
            result[j] = (rb_data_2019.loc[i]['gained_run']/16 + rb_data_2019.loc[j]['lost_run']/16)/2
        rb_run_matrix.loc[i] = result
    print(rb_run_matrix)

    # rb_run_matrix_norm = (rb_run_matrix-rb_run_matrix.mean())/rb_run_matrix.std()

    # heatmap
    sns.heatmap(rb_run_matrix, annot=True,fmt=".3g", annot_kws={"size": 7}, xticklabels=True, yticklabels=True, cmap='PuOr')
    # sns.heatmap(rb_run_matrix_norm, annot=True, annot_kws={"size": 7}, xticklabels=True, yticklabels=True, cmap='PuOr')
    plt.show()



def get_data(filename):
    return pd.read_csv(filename)

def save_csv(df, file_name):
    df.to_csv(file_name, index=False)


if __name__ == "__main__":
    main()
