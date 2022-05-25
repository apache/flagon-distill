from numpy import append
import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, callback
from dash import Dash, html, dcc
import plotly.express as px
from pandas import DataFrame
from pandas.io.parsers import TextFileReader
import plotly.figure_factory as ff
import dash_bootstrap_components as dbc

dash.register_page(__name__)
df = pd.read_csv("example_segments.csv")

fig_bubble = px.scatter(df.head(100),x="Start Time", y="End Time",
	         size="Number of Logs", color="Segment Type",
                 hover_name="Generate Matched Values")


app = Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])



layout = html.Div([
    
    html.P("bubble Chart"),
        dcc.Tab(label='bubble', children=[
            dcc.Graph(
                id='chrt-portfolio-main',
                figure = fig_bubble,
                style={'height': 550}),
            
            html.Hr(),
        
        
])
        ])