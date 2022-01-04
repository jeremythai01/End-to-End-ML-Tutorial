#! /usr/bin/env python
# -*- coding: utf-8 -*-

from decouple import config
from praw import Reddit
from praw.reddit import Comment, Submission
from typing import Any, List

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


    def scrape_reddit(self, subreddit: str, limit_posts: int):
        """Extract posts and comments by scraping data from specified subreddit.

        Parameters
        ----------
        subreddit :     string 
                        The subreddit where the bot will scrape data.

        limit_posts : integer 
                        The limit of posts where the bot will scrape data.
        
        Returns
        -------
        comments_info : list of scraped Reddit comments info
        """

        posts =  self._instance._bot.subreddit(subreddit).hot(limit=limit_posts)
        comments = self._scrape_comments(posts)

        return comments


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
            'post': str(comment.submission.title),
            'author': str(comment.author.name),
            'author_comment_karma': str(comment.author.comment_karma),
            'author_link_karma': str(comment.author.link_karma),
            'author_is_mod': str(comment.author.is_mod),
            'author_is_gold': str(comment.author.is_gold),
            'comment_id': str(comment.id),
            'body': str(comment.body),
            'score': str(comment.score),
            'date': str(comment.created_utc)
        }

        return comment_info


    def check_comment_constraints(self, comment: Any):
        # Filter comments without author or enough votes
        MIN_SCORE = 10
        return (type(comment) == Comment and 
                comment.author != None and 
                comment.score >= MIN_SCORE)


    def _scrape_comments(self, posts: List[Submission]):
        """Scrape Reddit comments from specified submissions.
        
        Parameters
        ----------
        posts :         list of Submission object 
                        The posts used to scrape data.      
        
        Returns
        -------
        comments_info : list of scraped Reddit comments info
        """
        comments_info = []
        i_c = 0
        for post in posts:
            # Include comments from the "load more comments" section
            post.comments.replace_more(limit=0)

            filtered_comments = list(filter(self.check_comment_constraints, post.comments.list()))
            for comment in filtered_comments:
                try:
                    c_info = self._extract_comment_info(comment)
                except AttributeError:
                    continue

                i_c += 1
                comments_info.append(c_info)
            print("1 post done")
                
        print(f'Scraped {i_c} comments')
        
        return comments_info