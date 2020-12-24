import praw
import configparser
import sys
from utilities.utils import create_reddit_bot
import stream

def main():

    reddit_bot = create_reddit_bot(config, praw)

    # Cmd line argument for desired subreddit
    submissions = reddit_bot.subreddit(sys.argv[1]).hot(limit=1000)
    
    stream_listener = stream.StreamListener(config, submissions)



    #Query data and store into CommentObject (one at a time?)



if __name__ == "__main__":
    main()
    
