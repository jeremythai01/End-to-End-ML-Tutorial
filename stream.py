import praw
import config
import mysql.connector
import datetime

class StreamListener():

    def __init__(self, config, submissions):
        self.submissions = submissions
        self.database = self.__connect_database(config)

    def __get_submission_info(self, submission):
        """This method will acquire the needed info for a reddit post"""
        return {
            'title': submission.title,
            'upvote_ratio': submission.upvote_ratio,
            'subreddit': submission.subreddit
        }


    def __get_comment_info(self, comment):
        """This method will acquire the needed info for reddit comments"""
        return {
            'body': comment.body, 
            'author': comment.author,
            'score': comment.score,
            'subreddit': comment.subreddit,
            'datetime': datetime.datetime.fromtimestamp(comment.created)
        }


    def __connect_database(self, config):

        try:
            database_config = config['database_config']
            # Connect to the database
            database = mysql.connector.connect(host=database_config['host'], 
                                        user=database_config['user'], 
                                        password=database_config['password'],
                                        port=database_config['port'], 
                                        database=database_config['database'], 
                                        auth_plugin=database_config['auth_plugin'])

        except mysql.connector.Error as error:
            print("Failed to insert record into Laptop table {}".format(error))
            quit()
        
        return database

    def stream_data(self):

        USE_QUERY = "USE Reddit"
        cursor = self.database.cursor()
        cursor.execute(USE_QUERY)

        # Loop through all posts retrieved from cmd line arguments. For each post iterate over all comments.
        # Store all of the data in database

        i_p = 0  
        i_c = 0
        for submission in self.submissions:
            if i_p % 5 == 0:
                print(f"Completed {i_p} posts")
            i_p += 1

            try:
                submission.comments.replace_more(limit=None)
                for comment in submission.comments.list():

                    if comment.author == "None":
                        continue

                    c_info = self.__get_comment_info(comment)
                    to_add = [c_info['body'], c_info['author'], c_info['score'], c_info['subreddit'], c_info['datetime']]
                    insert_query = """
                                    INSERT IGNORE INTO Comment 
                                    VALUES (DEFAULT, %s, %s, %s, %s, %s)
                                    """
                    cursor.execute(insert_query, to_add)
                    self.database.commit()
                    if i_c % 50 == 0 and i_c != 0:
                        print(f'Completed {i_c} comments')
                    i_c += 1

            except AttributeError:
                continue

        if self.database.is_connected():
            self.database.close()
            print("MySQL connection is closed")