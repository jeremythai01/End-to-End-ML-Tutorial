#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""The Dash app which will display a real-time graph of sentiment scores from 

the Reddit comments. It updates live sentiment scores by making HTTP requests

to the Flask API.
"""


import dash
import pandas as pd
import plotly
import requests
import time
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from decouple import config


app = dash.Dash(__name__)
app.layout = html.Div(
    [   html.H2('Live Reddit Stock Sentiment'),
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1*20000, # 1 second = 1000
            n_intervals= 0
        )
    ]
)

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])

def update_graph_scatter(n_intervals):

    response_stream = requests.post(f"{config('REST_API_URL')}stream")
    time.sleep(30)

    response_comments = requests.get(f"{config('REST_API_URL')}comments")

    comments = pd.DataFrame(response_comments.json())
    comments.sort_values('date', inplace=True)
    comments['sentiment'] = comments['sentiment'].rolling(int(len(comments)/5)).mean()

    X = comments.date.values[-100:]
    Y = comments.sentiment.values[-100:]

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),)}


if __name__ == '__main__':
    app.run_server(host=config('DASH_HOST'))  