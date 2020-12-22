'''
Written By: Ben McCoy, Dec 2020

This script uses plotly and dash to create an interactive dashboard showing nfl
statistics that runs un your browser and will eventually be published to
bashboard.fyi

TODO:
- Create a heatmap class
- Add Comments
- Generally tidy and restructure
- Format the dash webpage to be actually nice
- Make colours more consistent
- Nice to have - Time slider input (previous X games)
- Switch run yards data model to include run gaps and not directions
- Add the avg yards gained to graph #3
- Add the weekly form heatmap (Top 8, Top 16, Bottom 16)
- Deply to firebase
'''

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

import numpy as np
import argparse

class TeamTrend:
    def __init__(self):
        self.trend_df = self.get_trend_data()
        self.trend_df.rename(columns={'Unnamed: 1': 'delete'}, inplace=True)
        # print(self.trend_df)

    def get_trend_data(self):
        return pd.read_csv('../data/team_trends.csv', index_col=0)

    def trends_teams(self):
        return

class Heatmap:
    def __init__(self):
        # get heatmap data
        self.off_heatmap_df = self.get_heatmap_data('off', [2019])
        self.def_heatmap_df = self.get_heatmap_data('def', [2019])

        # get list of teams for dropdown
        self.teams = set(self.off_heatmap_df['Team'].tolist())

        # items required for plot
        self.labels_dict = dict(x='Play Direction', y='Play Types', color='Ranking')
        self.x_labels = ['Left', 'Middle', 'Right']
        self.y_labels = ['Long Pass', 'Short Pass', 'Run']

        # 3x3 plot and label arrays
        self.off_plot_array, self.off_labels_array = self.init_arrays()
        self.def_plot_array, self.def_labels_array = self.init_arrays()

        # add rankings to the heatmap dataframes
        self.gen_rankings_tables()

    def gen_rankings_tables(self):
        '''This function creates a copy of the heatmap data, then orders the
        table by each play type and direction and creates a new column with the
        rankings for each play type and directions.'''

        self.off_rank_table = self.off_heatmap_df.copy()
        for i in list(self.off_heatmap_df.columns):
            if i not in ['Team', 'Year']:
                self.off_rank_table.sort_values(by=i, inplace=True, ascending=False)
                col_name = i + ' rank'
                self.off_rank_table[col_name] = range(1, 33)

        self.def_rank_table = self.def_heatmap_df.copy()
        for i in list(self.def_heatmap_df.columns):
            if i not in ['Team', 'Year']:
                self.def_rank_table.sort_values(by=i, inplace=True, ascending=False)
                col_name = i + ' rank'
                self.def_rank_table[col_name] = range(1, 33)

    def get_heatmap_data(self, off_def, year):
        '''Get the aggregate offensive/defensive CSVs depending on off_def value,
        then aggregate based on the year and finally return dataframe'''

        if off_def == 'off':
            data = pd.read_csv('../data/agg_yards_off.csv')
        elif off_def == 'def':
            data = pd.read_csv('../data/agg_yards_def.csv')

        # TODO: be able to aggregate multiple years
        return data.loc[data['Year'].isin(year)]

    def init_arrays(self):
        '''Return two empty arrays of dimensions 3x3 to be used for plot colour
        mapping and label values'''

        plot_array = np.empty([3,3])
        labels_array = np.empty([3,3])

        return plot_array, labels_array

    def update_arrays(self, team):
        '''This function updates the offence and defence plot arrays with the latest selection of team'''

        # offence
        self.off_plot_array[0,0] = self.off_rank_table.loc[self.off_rank_table['Team'] == team, 'Pass long left rank'].iloc[0]
        self.off_plot_array[0,1] = self.off_rank_table.loc[self.off_rank_table['Team'] == team, 'Pass long middle rank'].iloc[0]
        self.off_plot_array[0,2] = self.off_rank_table.loc[self.off_rank_table['Team'] == team, 'Pass long right rank'].iloc[0]

        self.off_plot_array[1,0] = self.off_rank_table.loc[self.off_rank_table['Team'] == team, 'Pass short left rank'].iloc[0]
        self.off_plot_array[1,1] = self.off_rank_table.loc[self.off_rank_table['Team'] == team, 'Pass short middle rank'].iloc[0]
        self.off_plot_array[1,2] = self.off_rank_table.loc[self.off_rank_table['Team'] == team, 'Pass short right rank'].iloc[0]

        self.off_plot_array[2,0] = self.off_rank_table.loc[self.off_rank_table['Team'] == team, 'Run left rank'].iloc[0]
        self.off_plot_array[2,1] = self.off_rank_table.loc[self.off_rank_table['Team'] == team, 'Run middle rank'].iloc[0]
        self.off_plot_array[2,2] = self.off_rank_table.loc[self.off_rank_table['Team'] == team, 'Run right rank'].iloc[0]


        # defence
        self.def_plot_array[0,0] = self.def_rank_table.loc[self.def_rank_table['Team'] == team, 'Pass long left rank'].iloc[0]
        self.def_plot_array[0,1] = self.def_rank_table.loc[self.def_rank_table['Team'] == team, 'Pass long middle rank'].iloc[0]
        self.def_plot_array[0,2] = self.def_rank_table.loc[self.def_rank_table['Team'] == team, 'Pass long right rank'].iloc[0]

        self.def_plot_array[1,0] = self.def_rank_table.loc[self.def_rank_table['Team'] == team, 'Pass short left rank'].iloc[0]
        self.def_plot_array[1,1] = self.def_rank_table.loc[self.def_rank_table['Team'] == team, 'Pass short middle rank'].iloc[0]
        self.def_plot_array[1,2] = self.def_rank_table.loc[self.def_rank_table['Team'] == team, 'Pass short right rank'].iloc[0]

        self.def_plot_array[2,0] = self.def_rank_table.loc[self.def_rank_table['Team'] == team, 'Run left rank'].iloc[0]
        self.def_plot_array[2,1] = self.def_rank_table.loc[self.def_rank_table['Team'] == team, 'Run middle rank'].iloc[0]
        self.def_plot_array[2,2] = self.def_rank_table.loc[self.def_rank_table['Team'] == team, 'Run right rank'].iloc[0]

        # print(self.off_plot_array) # For Debugging

##########################################
''''''''''''''''''''''''''''''''''''''''''
''' ########## START PROGRAM ########## '''

# init Heatmap object to manage the heatmap plots and dataframes
heatmaps = Heatmap()

# init Trends object to manage the heatmap plots and dataframes
trends = TeamTrend()

# init the current team variable to optimise
curr_team = 'None'

# Start running the application
app = dash.Dash(__name__)

######################################
''' ######  HTML HERE ########### '''

# set up the layout of the page
app.layout = html.Div(className='row', children=[
    html.Div([
        html.Label(['Team']), # Text above dropdown
            dcc.Dropdown(
                id='off_team',
                options=[{"value": x, "label": x}
                            for x in heatmaps.teams], # TODO Set to a teams list in a class
                value='SEA'
            ),
    ]),

    html.Div(children=[ # setup line graph object
        dcc.Graph(id='off_heatmap', style={'display': 'inline-block'}),
        dcc.Graph(id='def_heatmap', style={'display': 'inline-block'})
    ]),

    html.Div(children=[ # setup histogram object
        dcc.Graph(id='off_linegraph', style={'display': 'inline-block'}),
        dcc.Graph(id='def_linegraph', style={'display': 'inline-block'})
    ]),

])



# Get input value from dropdown, return line_graph and histogram as figures
@app.callback(
    Output(component_id='off_heatmap', component_property='figure'),
    Output(component_id='def_heatmap', component_property='figure'),
    Output(component_id='off_linegraph', component_property='figure'),
    Output(component_id='def_linegraph', component_property='figure'),
    Input(component_id='off_team', component_property='value')
)
def update_figures(my_dropdown):
    # create figures to return to the call back

    ''' Strengths & Weaknesses Heatmaps #1 & #2'''

    if my_dropdown != curr_team:
        heatmaps.update_arrays(my_dropdown)

    fig1 = px.imshow(heatmaps.off_plot_array, labels=heatmaps.labels_dict, x=heatmaps.x_labels, y=heatmaps.y_labels, zmax=32, zmin=1, color_continuous_scale='rdylgn_r')
    fig2 = px.imshow(heatmaps.def_plot_array, labels=heatmaps.labels_dict, x=heatmaps.x_labels, y=heatmaps.y_labels, zmax=32, zmin=1, color_continuous_scale='rdylgn_r')

    ''' Weekly Yards Gained by Play Type Bar graph #3 '''

    df3 = trends.trend_df.loc[my_dropdown, :]
    # print(df3)
    fig3 = px.bar(df3, x='game_no', y='yards_gained', color='play_type', hover_name='play_direction')

    ''' Total yards gained by play type and play direction sunburst chart #4'''

    df4 = px.data.gapminder().query("year == 2007")
    # print(df4)
    fig4 = px.sunburst(df3, path=['play_type', 'play_direction'], values='yards_gained',
                        color_discrete_map={'run':'green', 'short_pass':'red', 'long_pass':'blue'})
    # fig.show()

    return fig1, fig2, fig3, fig4


if __name__ == "__main__":
    app.run_server(debug=True)
    # pass
