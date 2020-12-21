
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

def get_data(fname):
    '''get the data'''

    data = pd.read_csv(fname)
    return data


##########################################
''''''''''''''''''''''''''''''''''''''''''
''' ########## START PROGRAM ########## '''

# A bunc of crap to get the data ready
df_temp = get_data("../data/reg_pbp.csv")
print(df_temp)

# create DF used for plots
# df = pd.DataFrame(index=range(1,366))
# for index, row in df_temp.iterrows():
#     df.at[index.dayofyear, str(index)[:4]] = row.max_temp
#
# # start the app
# app = dash.Dash(__name__)
#
# # set up the layout of the page
# app.layout = html.Div([
#     html.Div([
#         html.Label(['Year']), # Text above dropdown
#         dcc.Dropdown( # init the dropdown
#             id='my_dropdown', # ID of this object
#             options=[ # User sees label, value is returned as input
#                      {'label': '1995', 'value': '1995'},
#                      {'label': '1996', 'value': '1996'},
#                      {'label': '1997', 'value': '1997'},
#                      {'label': '1998', 'value': '1998'},
#                      {'label': '1999', 'value': '1999'},
#                      {'label': '2000', 'value': '2000'},
#                      {'label': '2001', 'value': '2001'},
#                      {'label': '2002', 'value': '2002'},
#                      {'label': '2003', 'value': '2003'},
#                      {'label': '2004', 'value': '2004'},
#                      {'label': '2005', 'value': '2005'},
#                      {'label': '2006', 'value': '2006'},
#                      {'label': '2007', 'value': '2007'},
#                      {'label': '2008', 'value': '2008'},
#                      {'label': '2009', 'value': '2009'},
#                      {'label': '2010', 'value': '2010'},
#                      {'label': '2011', 'value': '2011'},
#                      {'label': '2012', 'value': '2012'},
#                      {'label': '2013', 'value': '2013'},
#                      {'label': '2014', 'value': '2014'},
#                      {'label': '2015', 'value': '2015'},
#                      {'label': '2016', 'value': '2016'},
#                      {'label': '2017', 'value': '2017'},
#                      {'label': '2018', 'value': '2018'},
#                      {'label': '2019', 'value': '2019'},
#                      {'label': '2020', 'value': '2020'},
#             ],
#             value='2019', # default value
#             multi=True,
#             clearable=False,
#             style={"width": "50%"}
#         ),
#     ]),
#
#     html.Div([ # setup line graph object
#         dcc.Graph(id='line_graph')
#     ]),
#
#     html.Div([ # setup histogram object
#         dcc.Graph(id='histogram')
#     ]),
#
# ])
#
# # Get input value from dropdown, return line_graph and histogram as figures
# @app.callback(
#     Output(component_id='line_graph', component_property='figure'),
#     Output(component_id='histogram', component_property='figure'),
#     Input(component_id='my_dropdown', component_property='value')
# )
#
# def display_time_series(my_dropdown):
#     # create figures to return to the call back
#     dff = df
#     line_fig = px.line(dff, x=dff.index, y=my_dropdown)
#     hist_fig = px.histogram(dff, x=my_dropdown, histnorm='probability')
#     return line_fig, hist_fig
#
# if __name__ == "__main__":
#     main()
#     app.run_server(debug=True)
#     # pass
