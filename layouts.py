import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, Event
from conf import colors

headline = html.H2('Live Sentiment', style={'color':colors['Headline']})
search_head = html.H5('Search: ', style={'color':colors['text']})
input_space = dcc.Input(id='ticker',value='TSLA',type='text',style={'color':colors['search_ticker']})