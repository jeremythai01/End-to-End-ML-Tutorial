import pandas as pd 
import datetime
class StreamHandler():

    def __init__(self, db_connection):
        self.__db_connection = db_connection

    def __get_comment_info(self, comment):
        """This method will acquire the needed info for reddit comments"""
        return {
            'subreddit': str(comment.subreddit),
            'author': str(comment.author),
            'body': str(comment.body), 
            'date': str(comment.created)
        }

    def stream_to_database(self, submissions):

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
                    to_add = [c_info['subreddit'], c_info['author'], c_info['body'], c_info['date']]
                    insert_query = """
                                    INSERT IGNORE INTO Comment 
                                    VALUES (DEFAULT, %s, %s, %s, %s)
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

        df = pd.DataFrame(raw_data,columns = ['body', 'date'])
        
        return df

    def close_db_connection(self):
        self.__db_connection.close()

    





        



