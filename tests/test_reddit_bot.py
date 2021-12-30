from services.data_scrape.app import reddit_bot


def test_getInstance():    
    
    bot_1 = reddit_bot.RedditBot.getInstance()
    bot_2 = reddit_bot.RedditBot.getInstance()

    assert bot_1 == bot_2
    

def test__scrape_reddit():
    bot = reddit_bot.RedditBot.getInstance()
    df = bot.scrape_reddit("Stocks", 3)

    assert [author != None for author in df.items()]