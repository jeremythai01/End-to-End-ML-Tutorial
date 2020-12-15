def create_reddit_bot(config, praw):
    #Create reddit instance
    bot_config = config['bot_config']
    reddit_bot = praw.Reddit(username=bot_config['username'],
                             password=bot_config['password'],
                             client_id=bot_config['client_id'],
                             client_secret=bot_config['client_secret'],
                             user_agent=bot_config['user_agent'])
    return reddit_bot