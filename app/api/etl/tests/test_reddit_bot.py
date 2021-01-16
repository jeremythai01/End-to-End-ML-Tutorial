import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import reddit_bot

def test_getInstance():

    reddit_bot_1 = reddit_bot.RedditBotSingleton.getInstance()
    reddit_bot_2 = reddit_bot.RedditBotSingleton.getInstance()

    assert reddit_bot_1 == reddit_bot

def test__scrape_reddit():
    reddit_bot = reddit_bot.RedditBotSingleton.getInstance()
    df = reddit_bot.scrape_reddit("Stocks", 3)

    assert df != None
    for author in df.items():
        assert author != None


    





