import dash
import random
import time
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from collections import deque
from dash.dependencies import Input, Output, Event

app = dash.Dash('vehicle-data')

GRAPH_MAX_LEN = 30
times=deque(maxlen=GRAPH_MAX_LEN)
oil_temps=deque(maxlen=GRAPH_MAX_LEN)
intake_temps=deque(maxlen=GRAPH_MAX_LEN)
coolant_temps=deque(maxlen=GRAPH_MAX_LEN)
rpms=deque(maxlen=GRAPH_MAX_LEN)
speeds=deque(maxlen=GRAPH_MAX_LEN)
throttle_pos=deque(maxlen=GRAPH_MAX_LEN)


data_dict = {'Oil Temperature':oil_temps,
'Intake Temperature': intake_temps,
'Coolant_Temperature': coolant_temps,
'RPM': rpms,
'Speed':speeds,
'Throttle Position': throttle_pos
}