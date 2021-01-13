import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly
import plotly.graph_objs as go
import pandas as pd
from configparser import ConfigParser
import mysql.connector
import os

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
        config = ConfigParser()
        path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
        config.read(os.path.join(path, 'database_config.ini'))
        database_config = config['database_config']

        try:
            # Connect to the database
            database = mysql.connector.connect(host=database_config['HOST'], 
                                        user=database_config['MYSQL_USER'], 
                                        password=database_config['MYSQL_PASSWORD'],
                                        port=database_config['MYSQL_PORT'], 
                                        database=database_config['MYSQL_DB'], 
                                        auth_plugin=database_config['MYSQL_AUTH_PLUGIN'])

        except mysql.connector.Error as error:
            print("Failed to insert record into Laptop table {}".format(error))
            quit()

        db_cursor = database.cursor()
        db_cursor.execute("USE Reddit")
        db_cursor.execute("SELECT date, sentiment FROM Comment ORDER BY date DESC LIMIT 500")

        data = db_cursor.fetchall()
        database.close()

        df = pd.DataFrame(data,columns = ['date', 'sentiment'])
        df['date'] = df['date'].astype(float)
        df.sort_values('date', inplace=True)

        df['sentiment'] = df['sentiment'].rolling(int(len(df)/5)).mean()

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
            f.write('nig\n')


if __name__ == '__main__':
    app.run_server(debug=True)  