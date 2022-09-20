#Pie Chart


import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, callback, State
from dash import Dash, html, dcc
import plotly.express as px
from pandas import DataFrame
from pandas.io.parsers import TextFileReader
import plotly.figure_factory as ff
import dash_bootstrap_components as dbc

dash.register_page(__name__)


df = pd.read_csv("example_segments.csv")

fig_pie = px.pie(df, values='Number of Logs', names='Segment Type')

layout = html.Div([
    html.H5('Pie Chart', className='text-center'),
            dcc.Graph(id='pie-top15',
                      figure = fig_pie.update_layout(template='plotly_dark'),
                      style={'height':380}),
            html.Hr()
])