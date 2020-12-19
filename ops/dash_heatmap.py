
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import argparse


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
            plot_array[i,j] = 32 - data.index.get_loc(team)
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

# def main():

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

# data = get_data(off_def, year)
# # print(data)

# # Get a list of the teams
# teams = set(data['Team'].tolist())
# # print(teams)

# plot_array, labels_array = init_arrays()
# # print(plot_array, labels_array)

# plot_array, labels_array = process_arrays(data, plot_array, labels_array, team)
# # print(plot_array, labels_array)

data = get_data(off_def, year)
teams = set(data['Team'].tolist())

app = dash.Dash(__name__)

app.layout = html.Div([

    html.P("OFF"),
    dcc.Dropdown(
        id='off_team',
        options=[{"value": x, "label": x}
                    for x in teams],
        value = 'SEA'
    ),
    dcc.Graph(id='off_graph'),

    html.P("DEF"),
    dcc.Dropdown(
        id='def_team',
        options=[{"value": x, "label": x}
                    for x in teams],
        value = 'SEA'
    ),
    dcc.Graph(id='def_graph'),
    
])

@app.callback(
    Output("off_graph", "figure"),
    [Input("off_team", 'value')])
def change_team(team):
    print(team)
    labels_dict = dict(x='Play Direction', y='Play Types', color='Ranking')
    x_labels = ['Left', 'Middle', 'Right']
    y_labels = ['Long Pass', 'Short Pass', 'Run']
    data = get_data(off_def, year)
    plot_array, labels_array = init_arrays()
    plot_array, labels_array = process_arrays(data, plot_array, labels_array, team)
    fig = px.imshow(plot_array, labels=labels_dict, x=x_labels, y=y_labels, zmax=32, zmin=1, color_continuous_scale='rdylgn_r')
    return fig

# # colors: rdylgn_r (best), tropic (not bad), temps (not bad), tealrose (not bad)
# labels_dict = dict(x='Play Direction', y='Play Types', color='Ranking')
# x_labels = ['Left', 'Middle', 'Right']
# y_labels = ['Long Pass', 'Short Pass', 'Run']
# fig = px.imshow(plot_array, labels=labels_dict, x=x_labels, y=y_labels, zmax=32, zmin=1, color_continuous_scale='rdylgn_r')
# fig.update_xaxes(side='top')
# fig.show()


if __name__ == "__main__":
    app.run_server(debug=True)
