import sys
from stream import StreamHandler
from reddit_bot import RedditBotSingleton
from database_connection import DBConnectionSingleton
def main():

    reddit_bot = RedditBotSingleton.getInstance()
    db_connection = DBConnectionSingleton.getInstance()

    while True: #Thread 
    
        # Cmd line argument for desired subreddit
        submissions = reddit_bot.get_bot().subreddit(sys.argv[1]).hot(limit=1000)
        
        stream_handler = StreamHandler(db_connection, submissions)

        stream_handler.stream_to_database()
    
        #Query data and store into CommentFactory



if __name__ == "__main__":
    main()
    
