from praw import Reddit
from decouple import config
import pandas as pd
from datetime import datetime, timezone

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
        
        reddit_bot = Reddit(username=config('REDDIT_USERNAME'),
                            password=config('REDDIT_PASSWORD'),
                            client_id=config('REDDIT_CLIENT_ID'),
                            client_secret=config('REDDIT_CLIENT_SECRET'),
                            user_agent=config('REDDIT_USER_AGENT'))

        return reddit_bot


    def scrape_reddit(self, subreddit, size):
        submissions =  self.__bot.subreddit(subreddit).hot(limit=size)
        df = self.__create_dataframe(submissions)
        return df

    def __get_comment_info(self, comment):
        """This method will acquire the needed info for reddit comments"""
        return {
            'subreddit': str(comment.subreddit),
            'author': str(comment.author),
            'text': str(comment.body), 
            'date': self.__convert_time_zones(comment.created)
        }

    def __convert_time_zones(self, date):
        utc_dt = datetime.utcfromtimestamp(date)
        local_dt = utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
        return local_dt.strftime('%Y-%m-%d %H:%M:%S')

    def __create_dataframe(self, submissions):
        columns = ['subreddit', 'author', 'text', 'date']
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