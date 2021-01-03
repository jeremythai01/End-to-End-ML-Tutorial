import datetime

class Comment():

    def __init__(self, subreddit, author, body, score, datetime):
        self.__subreddit = subreddit
        self.__author = author
        self.__body = body
        self.__score = score
        self.__datetime = datetime
        

    def get_body(self):
        return self.__body

    