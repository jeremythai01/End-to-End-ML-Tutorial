import sys
from stream_handler import StreamHandler
from reddit_bot import RedditBotSingleton
from database_connection import DBConnectionSingleton
from src.ml.model import SentimentAnalysisSVM

def run_etl():

    reddit_bot = RedditBotSingleton.getInstance()
    db_connection = DBConnectionSingleton.getInstance()
    stream_handler = StreamHandler(db_connection)
    sentiment_analyzer = SentimentAnalysisSVM()

    try:
        while True:
                submissions = reddit_bot.scrape_reddit("Stocks", 3)
                df = reddit_bot.create_dataframe(submissions)
                df = sentiment_analyzer.predict_sentiment(df)
                stream_handler.stream_to_database(df)

    except KeyboardInterrupt:
        stream_handler.close_db_connection()
        sys.exit(0)

if __name__ == "__main__":
    run_etl()
    
