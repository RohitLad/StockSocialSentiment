import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

layout_old = html.Div([

    html.H1(('Stock Tickers')),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Coke', 'value': 'COKE'},
            {'label': 'Tesla', 'value': 'TSLA'},
            {'label': 'Apple', 'value': 'AAPL'}
        ],
        value='COKE'        
    ),
    dcc.Graph(id='my-graph')
], style={'width':'500'})


'''layout'''


layout = html.Div([

    dcc.Interval(id="query_update",
                interval=int(2000),
                n_intervals=0,),

    html.Div([
        html.H6('SENTIMENT SCORE', className='graph_title')
    ]),
    dcc.Graph(
        id='sentiment_scores',
        figure=go.Figure(
            layout=go.Layout(
                plot_bgcolor="rgb(221, 236, 255)",
                paper_bgcolor="rgb(221, 236, 255)",
            )
        )
    )

], className="graph_container")