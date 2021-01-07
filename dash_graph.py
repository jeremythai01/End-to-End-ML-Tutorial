import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly
import plotly.graph_objs as go
import pandas as pd
from database_connection import DBConnectionSingleton


app = dash.Dash(__name__)
app.layout = html.Div(
    [   html.H2('Live Reddit Stock Sentiment'),
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1*1000,
            n_intervals= 0
        ),
    ]
)

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])

def update_graph_scatter(n_intervals):
    try:
        db_connection = DBConnectionSingleton.getInstance()
        db_connection.query("SELECT date, sentiment FROM Comment ORDER BY date DESC LIMIT 100")
        data = db_connection.fetchall()
        df = pd.DataFrame(data,columns = ['date', 'sentiment'])
        df['date'] = df['date'].astype(float)
        df.sort_values('date', inplace=True)
        df['sentiment'] = df['sentiment'].rolling(int(len(df)/5)).mean()
        df.dropna(inplace=True)
        X = df.date.values[-100:]
        Y = df.sentiment.values[-100:]

        data = plotly.graph_objs.Scatter(
                x=list(X),
                y=list(Y),
                name='Scatter',
                mode= 'lines+markers'
                )

        return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                    yaxis=dict(range=[min(Y),max(Y)]),)}

    except Exception as e:
        with open('errors.txt','a') as f:
            f.write(str(e))
            f.write('\n')

    

if __name__ == '__main__':
    app.run_server(debug=True)

    