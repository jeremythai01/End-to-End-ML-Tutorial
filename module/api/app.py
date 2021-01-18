#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""The Flask Rest API which will receive HTTP requests from the Dash app,

interact with the MySQL database and serve the machine learning model for 

real-time inference.
"""


from decouple import config
from flask import Flask
from flask import jsonify
from etl.reddit_bot import RedditBotSingleton
from etl.stream_handler import StreamHandler
from ml.model import SentimentAnalysisModel

reddit_bot = RedditBotSingleton.getInstance()
stream_handler = StreamHandler()
sentiment_analyzer = SentimentAnalysisModel()
LIMIT_NUMBER_SUBREDDITS = 5
LIMIT_NUMBER_COMMENTS = 500

app = Flask(__name__)

@app.route('/stream', methods=['POST'])
def stream():

    df = reddit_bot.scrape_reddit("Stocks", LIMIT_NUMBER_SUBREDDITS)
    df = sentiment_analyzer.predict_sentiment(df)
    stream_handler.stream_to_database(df)

    return jsonify("OK")

@app.route('/comments', methods=['GET'])
def get_comments():
  
    query = stream_handler.retrieve_data(LIMIT_NUMBER_COMMENTS)
    
    return jsonify([stream_handler.serialize(row) for row in query])


if __name__ == '__main__':
    
    app.run(host=config('REST_API_HOST'))