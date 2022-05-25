
import dash
# Code from: https://github.com/plotly/dash-labs/tree/main/docs/demos/multi_page_example1
dash.register_page(__name__)

import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, callback, State
from dash import Dash, html, dcc
import plotly.express as px
from pandas import DataFrame
from pandas.io.parsers import TextFileReader
import plotly.figure_factory as ff
import dash_bootstrap_components as dbc

df = pd.read_csv("example_segments.csv")

fig_bar = px.histogram(df, x="Segment Type", y="Number of Logs",
             color='Segment Type', barmode='group',
             histfunc='avg',
             height=400)

layout = html.Div(
    [
        html.H5('Bar Chart', className='text-center'),
            dcc.Graph(id='indicators-ptf',
                      figure = fig_bar.update_layout(template='plotly_dark')
            
        ),
       
    ]
)


