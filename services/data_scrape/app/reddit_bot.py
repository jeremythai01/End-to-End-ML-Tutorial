#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
#import boto3
from decouple import config
from praw import Reddit
from praw.reddit import Comment, Submission
from typing import List
from app.schemas import Comment
from app.utils import convert_time_zone, get_dt_now

#s3_client = boto3.client("s3")
S3_BUCKET = "your-s3-bucket"

class RedditBot:
    """Reddit bot singleton to scrape Reddit data from subreddits."""
    _instance = None

    @staticmethod 
    def getInstance():
        """Static access method."""
        if RedditBot._instance == None:
            RedditBot()

        return RedditBot._instance


    def __init__(self):
        """Virtually private constructor."""
        if RedditBot._instance != None:
            raise Exception("This class is a singleton!")
        else:
            RedditBot._instance = self
            RedditBot._instance._bot = self._create_reddit_bot()


    def _create_reddit_bot(self):
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


    def scrape_reddit(self, subreddit: str, n_submissions: int):
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
        submissions =  self._instance._bot.subreddit(subreddit).hot(limit=n_submissions)
        df = self._scrape_comments(submissions)

        return df


    def _extract_comment_info(self, comment: Comment):
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
            'date': convert_time_zone(comment.created)
        }

        return comment_info


    def _scrape_comments(self, submissions: List[Submission]):
        """Scrape Reddit comments from specified submissions.
        
        Parameters
        ----------
        submissions : list of Submission object 
                      The submissions used to scrape data.      
        
        Returns
        -------
        df : dataframe of scraped Reddit comments
        """
        comments = []
        i_c = 0
        MIN_VOTES = 5
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

                    c_info = self._extract_comment_info(comment)
                    comments.append(c_info)
                    i_c += 1

            except AttributeError:
                continue

        print(f'Scraped {i_c} comments')
        
        return comments

    def upload_to_s3(self, comments: List[Comment]):

        location = "/tmp"
        filename = get_dt_now() + ".json"
        local_filepath = location + "/" + filename

        # Write to local 
        with open(local_filepath, "w") as jsonFile:
                json.dump(comments, jsonFile)

        # Upload to AWS S3 bucket
        #s3_client.upload_file(local_filepath, S3_BUCKET, filename)