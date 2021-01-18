from etl import reddit_bot


def test_getInstance():    
    
    bot_1 = reddit_bot.RedditBotSingleton.getInstance()
    bot_2 = reddit_bot.RedditBotSingleton.getInstance()

    assert bot_1 == bot_2
    

def test__scrape_reddit():
    bot = reddit_bot.RedditBotSingleton.getInstance()
    df = bot.scrape_reddit("Stocks", 3)

    assert [author != None for author in df.items()]