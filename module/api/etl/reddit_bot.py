#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from decouple import config
from datetime import datetime
from datetime import timezone
from praw import Reddit


class RedditBotSingleton:
    """Reddit bot singleton to scrape Reddit data from subreddits."""
    __instance = None

    @staticmethod 
    def getInstance():
        """Static access method."""
        if RedditBotSingleton.__instance == None:
            RedditBotSingleton()

        return RedditBotSingleton.__instance


    def __init__(self):
        """Virtually private constructor."""
        if RedditBotSingleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            RedditBotSingleton.__instance = self
            RedditBotSingleton.__instance.__bot = self.__create_reddit_bot()


    def __create_reddit_bot(self):
        """Create Reddit bot instance.

        Returns
        -------
        reddit_bot : new reddit bot instance
        """
        reddit_bot = Reddit(username=config('REDDIT_USERNAME'),
                            password=config('REDDIT_PASSWORD'),
                            client_id=config('REDDIT_CLIENT_ID'),
                            client_secret=config('REDDIT_CLIENT_SECRET'),
                            user_agent=config('REDDIT_USER_AGENT'))

        return reddit_bot


    def scrape_reddit(self, subreddit, n_submissions):
        """Extract submissions and scrape data from specified subreddit.

        Parameters
        ----------
        subreddit :     string 
                        The subreddit where the bot will scrape data.

        n_submissions : integer 
                        The number of posts where the bot will scrape data.
        
        Returns
        -------
        df : dataframe of scraped Reddit comments
        """
        submissions =  self.__bot.subreddit(subreddit).hot(limit=n_submissions)
        df = self.__scrape_comments(submissions)

        return df


    def __extract_comment_info(self, comment):
        """Extract the needed info for reddit comments.
        
        Parameters
        ----------
        comment : Comment object
                  The comment used to extract the info.     
        
        Returns
        -------
        comment_info : dict of the comment info
        """
        comment_info = {
            'subreddit': str(comment.subreddit),
            'author': str(comment.author),
            'text': str(comment.body), 
            'date': self.__convert_time_zone(comment.created)  # Convert timezone
        }

        return comment_info


    def __convert_time_zone(self, date):
        """Convert time zone to local time.
        
        Parameters
        ----------
        date : UNIX format 
               The date to be changed to local time.     
        
        Returns
        -------
        local_datetime : datetime adjusted according to local time zone
        """
        utc_datetime = datetime.utcfromtimestamp(date)
        local_datetime = utc_datetime.replace(tzinfo=timezone.utc).astimezone(tz=None)
        local_datetime = local_datetime.strftime('%Y-%m-%d %H:%M:%S')
        
        return local_datetime


    def __scrape_comments(self, submissions):
        """Scrape Reddit comments from specified submissions.
        
        Parameters
        ----------
        submissions : list of Submission object 
                      The submissions used to scrape data.      
        
        Returns
        -------
        df : dataframe of scraped Reddit comments
        """
        columns = ['subreddit', 'author', 'text', 'date']
        df = pd.DataFrame(columns=columns)
        i_c = 0
        MIN_VOTES = 2
        for submission in submissions:
            try:
                
                # Exclude irrelevant submissions
                if any(substring in submission.title for substring in 
                      ('Thread', 'Daily Discussion', 'Porfolio')):
                    continue 

                # Include comments from the "load more comments" section
                submission.comments.replace_more(limit=None)
                for comment in submission.comments.list():

                    # Filter comments without author or enough votes
                    if comment.author == "None" or comment.score < MIN_VOTES:
                        continue

                    c_info = self.__extract_comment_info(comment)
                    df = df.append(c_info, ignore_index=True)
                 
                    i_c += 1

            except AttributeError:
                continue

        print(f'Scraped {i_c} comments')
        
        return df