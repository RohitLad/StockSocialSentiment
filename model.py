import os
import dash
import sqlite3
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Output, Input, Event
from conf import *
from layouts import *

'''connecting to the database'''
#connection = sqlite3(DB_NAME, check_same_thread = False)


''' Creating Dash app'''
app = dash.Dash(__name__)

'''defining layout'''
app.layout = html.Div([
    html.Div(className='container-fluid', children=[headline, search_head, input_space],style=container_fluid_style),
    html.Div(className='row', children=[html.Div(dcc.Graph(id='live-graph', animate=False), className='col s12 m6 l6'),
                                        html.Div(dcc.Graph(id='historical-graph', animate=False), className='col s12 m6 l6')]),

    html.Div(className='row', children=[html.Div(id="recent-tweets-table", className='col s12 m6 l6'),
                                        html.Div(dcc.Graph(id='sentiment-pie', animate=False), className='col s12 m6 l6')]),
    dcc.Interval(id='recent-table-update', interval=2*1000),

])


@app.callback(Output('recent-tweets-table','children'),[Input(component_id='ticker', component_property='value')], events=[Event('recent-table-update','interval')])
def update_recent_tweets(ticker):
    if ticker:
        df = pd.read_sql('SELECT sentiment.* FROM sentiment_fts fts LEFT JOIN sentiment ON fts.rowid= sentiment.id WHERE fts.sentiment_fts MATCH ? ORDER BY fts.rowid DESC LIMIT 10')

server = app.server
dev_server = app.run_server