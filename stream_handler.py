import datetime
from comment import Comment
class StreamHandler():

    def __init__(self, db_connection):
        self.__db_connection = db_connection
        self.__comment_set = set()

    def __get_comment_info(self, comment):
        """This method will acquire the needed info for reddit comments"""
        return {
            'subreddit': str(comment.subreddit),
            'author': str(comment.author),
            'body': comment.body, 
            'score': comment.score,
            'datetime': datetime.datetime.fromtimestamp(comment.created)
        }

    def stream_to_database(self, submissions):

        i_c = 0
        for submission in submissions:
            try:

                if "Thread" in submission.title or "Daily Discussion" in submission.title:
                    continue 

                submission.comments.replace_more(limit=None)
                for comment in submission.comments.list():

                    if comment.author == "None" or comment.score <= 1:
                        continue

                    c_info = self.__get_comment_info(comment)
                    to_add = [c_info['subreddit'], c_info['author'], c_info['body'], c_info['score'], c_info['datetime']]
                    insert_query = """
                                    INSERT IGNORE INTO Comment 
                                    VALUES (DEFAULT, %s, %s, %s, %s, %s)
                                    """
                    self.__db_connection.query(insert_query, to_add)
                    self.__db_connection.commit()
                    i_c += 1

            except AttributeError:
                continue

        print(f'Completed {i_c} comments')
                    

    def import_from_database(self, query):

        self.__db_connection.query(query) #Query data
        raw_data = self.__db_connection.fetchall()

        for row in raw_data:
            comment = Comment(row[0], row[1], row[2], row[3], row[4])
            self.__comment_set.add(comment)

    def get_comment_set(self):
        return self.__comment_set

    def close_db_connection(self):
        self.__db_connection.close()

    





        



