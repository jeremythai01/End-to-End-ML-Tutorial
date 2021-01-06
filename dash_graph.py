import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly
import random
import plotly.graph_objs as go
import pandas as pd
from collections import deque
import sys
import time
from stream_handler import StreamHandler
from reddit_bot import RedditBotSingleton
from database_connection import DBConnectionSingleton
from sentiment_analysis import SentimentAnalysis

# X = deque(maxlen = 20) 
# X.append(1) 
  
# Y = deque(maxlen = 20) 
# Y.append(1) 

#Global variable
sentiment_df = None

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

        X = sentiment_df.date.values[-100:]
        Y = sentiment_df.sentiment.values[-100:]

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


def run_program():

    reddit_bot = RedditBotSingleton.getInstance()
    db_connection = DBConnectionSingleton.getInstance()
    stream_handler = StreamHandler(db_connection)
    sentiment_analyzer = SentimentAnalysis()
    ONE_MINUTE = 60.0        

    try:
       while True:
           
            if is_app_running == True:
                start_time = time.time()
                time.sleep(ONE_MINUTE - ((time.time() - start_time) % ONE_MINUTE)) 

            print("Scraping data from r/Stocks")
            submissions = reddit_bot.scrape_reddit("stocks", 3)
            
            print("Streaming data to database...")
            stream_handler.stream_to_database(submissions)

            print("Loading data from database...")
            df = stream_handler.import_from_database("SELECT body, date FROM Comment ORDER BY date DESC LIMIT 500")

            print("Sentiment analysis...")
        
            global sentiment_df
            sentiment_df = sentiment_analyzer.sentiment_score(df)  

    except KeyboardInterrupt:
        stream_handler.close_db_connection()
        sys.exit(0)

if __name__ == '__main__':
    app.run_server(debug=True)
    run_program()
    
    