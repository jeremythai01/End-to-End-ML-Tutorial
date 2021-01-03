from praw import Reddit
from configparser import ConfigParser
class RedditBotSingleton:

    __instance = None

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if RedditBotSingleton.__instance == None:
            RedditBotSingleton()

        return RedditBotSingleton.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if RedditBotSingleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            RedditBotSingleton.__instance = self
            RedditBotSingleton.__instance.__bot = self.__create_reddit_bot()


    def __create_reddit_bot(self):
        #Create reddit instance
        
        config = ConfigParser()
        config.read('config.ini')
        bot_config = config['bot_config']
        reddit_bot = Reddit(username=bot_config['username'],
                            password=bot_config['password'],
                            client_id=bot_config['client_id'],
                            client_secret=bot_config['client_secret'],
                            user_agent=bot_config['user_agent'])

        return reddit_bot


    def scrape_reddit(self, subreddit, size):
        return self.__bot.subreddit(subreddit).hot(limit=size)