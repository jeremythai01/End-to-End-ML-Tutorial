from praw import Reddit
from configparser import ConfigParser
import pandas as pd
import os

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
        path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
        config.read(os.path.join(path, 'bot_config.ini'))
        bot_config = config['bot_config']
        reddit_bot = Reddit(username=bot_config['USERNAME'],
                            password=bot_config['PASSWORD'],
                            client_id=bot_config['CLIENT_ID'],
                            client_secret=bot_config['CLIENT_SECRET'],
                            user_agent=bot_config['USER_AGENT'])

        return reddit_bot


    def scrape_reddit(self, subreddit, size):
        return self.__bot.subreddit(subreddit).hot(limit=size)

    def __get_comment_info(self, comment):
        """This method will acquire the needed info for reddit comments"""
        return {
            'subreddit': str(comment.subreddit),
            'author': str(comment.author),
            'body': str(comment.body), 
            'date': str(comment.created)
        }


    def create_dataframe(self, submissions):
        columns = ['subreddit', 'author', 'body', 'date']
        df = pd.DataFrame(columns=columns)
        i_c = 0
        for submission in submissions:
            try:

                if any(substring in submission.title for substring in ('Thread', 'Daily Discussion', 'Porfolio')):
                    continue 

                submission.comments.replace_more(limit=None)
                for comment in submission.comments.list():

                    if comment.author == "None" or comment.score < 2:
                        continue

                    c_info = self.__get_comment_info(comment)
                    df = df.append(c_info, ignore_index=True)
                 
                    i_c += 1

            except AttributeError:
                continue

        print(f'Scraped {i_c} comments')
        
        return df