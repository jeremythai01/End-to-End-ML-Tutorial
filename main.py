import sys
import time
from stream_handler import StreamHandler
from reddit_bot import RedditBotSingleton
from database_connection import DBConnectionSingleton
from sentiment_analysis import SentimentAnalysis
from graph import Graph

def run_program(reddit_bot, db_connection, stream_handler, sentiment_analyzer, graph):

    print("Scraping data ...")
    submissions = reddit_bot.scrape_reddit("Bitcoin", 3)
    
    print("Streaming data to database...")
    stream_handler.stream_to_database(submissions)

    print("Loading data from database...")
    stream_handler.import_from_database("SELECT subreddit, author, body, score, datetime FROM Comment")

    print("Sentiment analysis...")
    results = sentiment_analyzer.sentiment(stream_handler.get_comment_set())

    print("Displaying graph...")
    graph.set_graph_data(results)
    graph.display()

    print("Waiting for next iteration")

def main():

    reddit_bot = RedditBotSingleton.getInstance()
    db_connection = DBConnectionSingleton.getInstance()
    stream_handler = StreamHandler(db_connection)
    sentiment_analyzer = SentimentAnalysis()
    graph = Graph()
    start_time = time.time()
    TEN_MINUTES = 600.0

    while True:
        try:
            run_program(reddit_bot, db_connection, stream_handler, sentiment_analyzer, graph)
            time.sleep(TEN_MINUTES - ((time.time() - start_time) % TEN_MINUTES))  

        except KeyboardInterrupt:
            stream_handler.close_db_connection()
            sys.exit(0)

if __name__ == "__main__":
    main()
    
