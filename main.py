import sys
import time
from stream_handler import StreamHandler
from reddit_bot import RedditBotSingleton
from database_connection import DBConnectionSingleton
from sentiment_analysis import SentimentAnalysis

def run_program(reddit_bot, db_connection, stream_handler, sentiment_analyzer):

    print("Scraping data from", sys.argv[1])
    submissions = reddit_bot.scrape_reddit(sys.argv[1], 3)
    
    print("Streaming data to database...")
    stream_handler.stream_to_database(submissions)

    print("Loading data from database...")
    df = stream_handler.import_from_database("SELECT body, date FROM Comment")

    print("Sentiment analysis...")
    sentiment_analyzer.sentiment_score(df)

    # print("Displaying graph...")
    # graph.set_graph_data(score)
    # graph.display()

    print("Waiting for next iteration")

def main():

    reddit_bot = RedditBotSingleton.getInstance()
    db_connection = DBConnectionSingleton.getInstance()
    stream_handler = StreamHandler(db_connection)
    sentiment_analyzer = SentimentAnalysis()
    ONE_MINUTE = 600.0

    try:
        while True:
                run_program(reddit_bot, db_connection, stream_handler, sentiment_analyzer)
                start_time = time.time()
                time.sleep(ONE_MINUTE - ((time.time() - start_time) % ONE_MINUTE))  

    except KeyboardInterrupt:
        stream_handler.close_db_connection()
        sys.exit(0)

if __name__ == "__main__":
    main()
    
