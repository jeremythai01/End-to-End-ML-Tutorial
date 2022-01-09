"""The Dash app which will display a real-time graph of sentiment scores from 

the Reddit comments. It updates live sentiment scores by fetching data from AWS RDS.
"""

import dash
import pandas as pd
import plotly
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from decouple import config
from warehouse_connection import WarehouseConnection
from helpers import *

warehouse_connection = WarehouseConnection.getInstance()

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

    data = warehouse_connection.fetch(get_sentiment_select_query())

    df_sentiment = pd.DataFrame.from_records(dict(row) for row in data)

    df_sentiment['score'] = df_sentiment['score'].rolling(int(len(df_sentiment)/5)).mean()

    X = df_sentiment.date.values[-100:]
    Y = df_sentiment.sentiment.values[-100:]

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),)}


if __name__ == '__main__':
    app.run_server(host='0.0.0.0')