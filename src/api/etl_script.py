import sys
from etl.stream_handler import StreamHandler
from etl.reddit_bot import RedditBotSingleton
from etl.database_connection import DBConnectionSingleton
from ml.model import SentimentAnalysisModel

def run_etl():

    reddit_bot = RedditBotSingleton.getInstance()
    db_connection = DBConnectionSingleton.getInstance()
    stream_handler = StreamHandler(db_connection)
    sentiment_analyzer = SentimentAnalysisModel()

    try:
        while True:
                df = reddit_bot.scrape_reddit("Stocks", 10)
                df = sentiment_analyzer.predict_sentiment(df)
                stream_handler.stream_to_database(df)

    except KeyboardInterrupt:
        stream_handler.close_db_connection()
        sys.exit(0)

if __name__ == "__main__":
    run_etl()