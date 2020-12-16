import praw
import configparser
import sys
from .utility.utilitys import create_reddit_bot

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    reddit_bot = create_reddit_bot(config, praw)

    # get 10 hot posts from the MachineLearning subreddit
    hot_posts = reddit_bot.subreddit('CanadianInvestor').hot(limit=10)
    for post in hot_posts:
        print(post.title)

if __name__ == "__main__":
    main()
    
