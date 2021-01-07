import sys
import time
from stream_handler import StreamHandler
from reddit_bot import RedditBotSingleton
from database_connection import DBConnectionSingleton
from sentiment_analysis import SentimentAnalysis

def run_program(reddit_bot, db_connection, stream_handler, sentiment_analyzer):

    submissions = reddit_bot.scrape_reddit("Stocks", 3)
    df = reddit_bot.create_dataframe(submissions)

    df = sentiment_analyzer.sentiment_score(df)

    stream_handler.stream_to_database(df)

def main():

    is_server_running = False
    reddit_bot = RedditBotSingleton.getInstance()
    db_connection = DBConnectionSingleton.getInstance()
    stream_handler = StreamHandler(db_connection)
    sentiment_analyzer = SentimentAnalysis()
    ONE_MINUTE = 60.0

    try:
        while True:
                run_program(reddit_bot, db_connection, stream_handler, sentiment_analyzer)

                #if is_server_running == False:
                    #execfile('dash_graph.py')
                # start_time = time.time()
                # time.sleep(ONE_MINUTE - ((time.time() - start_time) % ONE_MINUTE))  

    except KeyboardInterrupt:
        stream_handler.close_db_connection()
        sys.exit(0)

if __name__ == "__main__":
    main()
    
