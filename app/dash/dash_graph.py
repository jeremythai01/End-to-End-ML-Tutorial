import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly
import plotly.graph_objs as go
import pandas as pd
import requests
import time
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

    # response_stream = requests.post(f"{config['API_URL']}/stream")
    # time.sleep(30)
    

    response_comments = requests.get(f"{config['API_URL']}/comments")

    # with open('errors.txt','a') as f:
    #     if response_stream.ok:
    #         f.write("Streamed successfully\n")
    #         response_comments = requests.get(f"{config['API_URL']}/comments")
    #         if response_comments.ok:
    #             f.write("Loaded successfully\n")
    #         else:
    #             f.write("error load\n")
    #     else:
    #         f.write("error stream\n")

    comments = pd.DataFrame(response_comments.json())
    comments['date'] = comments['date'].astype(float)
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