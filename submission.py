from comment import Comment

class Submission():

    def __init__(self, title, upvote_ratio, subreddit):
        self.__title = title
        self.__upvote_ratio = upvote_ratio
        self.__subreddit = subreddit
        self.__comment_set = set()

    def get_comments(self):
        return self.__comment_set

    def add_comment(self, comment):
        self.__comment_set.add(comment)

    def get_title(self):
        return self.__title




    
    