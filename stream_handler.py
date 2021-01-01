import datetime
from submission import Submission
from comment import Comment

class StreamHandler():

    def __init__(self, db_connection, submissions):
        self.__db_connection = db_connection
        self.__submissions = submissions
        self.__submission_set = set()
       
    def __get_submission_info(self):
        """This method will acquire the needed info for a reddit post"""
        return {
            'iddb_connectionitle': self.__submissions.title,
            'upvote_ratio': self.__submissions.upvote_ratio,
            'subreddit': self.__submissions.subreddit
        }


    def __get_comment_info(self, comment):
        """This method will acquire the needed info for reddit comments"""
        return {
            'body': comment.body, 
            'author': comment.author,
            'score': comment.score,
            'datetime': datetime.datetime.fromtimestamp(comment.created)
        }

    def stream_to_database(self):

        USE_QUERY = "USE Reddit"
        self.__db_connection.query(USE_QUERY)

        # Loop through all posts retrieved from cmd line arguments. For each post iterate over all comments.
        # Store all of the data in database

        i_s = 0  
        i_c = 0
        for submission in self.__submissions:
            s_info = self.__get_submission_info()
            to_add = [s_info['id'], s_info['title'], s_info['upvote_ratio'], s_info['subreddit']]
            insert_query = """
                            INSERT IGNORE INTO Comment 
                            VALUES (DEFAULT, %s, %s, %s, %s)
                            """
            self.__db_connection.query(insert_query, to_add)
            if i_s % 5 == 0:
                print(f"Completed {i_s} posts")
            i_s += 1

            try:
                submission.comments.replace_more(limit=None)
                for comment in submission.comments.list():

                    if comment.author == "None":
                        continue

                    c_info = self.__get_comment_info(comment)
                    to_add = [s_info['id'], c_info['body'], c_info['author'], c_info['score'], c_info['datetime']]
                    insert_query = """
                                    INSERT IGNORE INTO Comment 
                                    VALUES (DEFAULT, %s, %s, %s, %s, %s)
                                    """
                    self.__db_connection.query(insert_query, to_add)
                    if i_c % 50 == 0 and i_c != 0:
                        print(f'Completed {i_c} comments')
                    i_c += 1

            except AttributeError:
                continue

    def add_submission(self, submission):
        self.__submission_set.add(submission)

    def import_from_database(self, query):

        self.__db_connection.query(query) #Query data
        raw_data = self.__db_connection.fetchall()
        for row in raw_data:
            submission = Submission(row[1], row[2], row[3])
            self.__db_connection.query("") #Query comments using foreign key
            raw_comments = self.__db_connection.fetchall()
            for data in raw_comments:
                comment = Comment(data[1], data[2], data[3], data[4])
                submission.add_comment(comment)

            self.add_submission(submission)

    





        



