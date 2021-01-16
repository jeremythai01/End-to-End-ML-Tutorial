from flask import Flask, jsonify, request
from etl.reddit_bot import RedditBotSingleton
from etl.stream_handler import StreamHandler
from etl.database_connection import DBConnectionSingleton
from ml.model import SentimentAnalysisSVM
from decouple import config
import warnings

reddit_bot = RedditBotSingleton.getInstance()
db_connection = DBConnectionSingleton.getInstance()
stream_handler = StreamHandler(db_connection)
warnings.filterwarnings(action="ignore", message="Trying to unpickle estimator ")
sentiment_analyzer = SentimentAnalysisSVM()
LIMIT_NUMBER_SUBREDDITS = 5
LIMIT_NUMBER_COMMENTS = 500

app = Flask(__name__)

@app.route('/stream', methods=['POST'])
def stream():

    df = reddit_bot.scrape_reddit("Stocks", LIMIT_NUMBER_SUBREDDITS)
    df = sentiment_analyzer.predict_sentiment(df)
    stream_handler.stream_to_database(df)

    return "resolved"

@app.route('/comments', methods=['GET'])
def get_comments():
  
    query = stream_handler.load_data(LIMIT_NUMBER_COMMENTS)
    return jsonify([stream_handler.serialize(row) for row in query])


if __name__ == '__main__':
    app.run(host=config('MYSQL_HOST'))