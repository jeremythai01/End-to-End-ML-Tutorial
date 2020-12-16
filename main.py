import praw
import configparser
import sys
from utilities.utils import create_reddit_bot
import mysql.connector
import datetime
def get_submission_info(submission):
    """This method will acquire the needed info for a reddit post"""
    return {
        'title': submission.title,
        'upvote_ratio': submission.upvote_ratio, 
    }


def get_comment_info(comment):
    """This method will acquire the needed info for reddit comments"""
    return {
        'body': comment.body, 
        'author': comment.author,
        'score': comment.score,
        'subreddit': comment.subreddit,
        'datetime': datetime.datetime.fromtimestamp(comment.created)
    }


def connect_database(config, submissions):
    try:
        database_config = config['database_config']
        # Connect to the database
        db = mysql.connector.connect(host=database_config['host'], 
                                     user=database_config['user'], 
                                     password=database_config['password'],
                                     port=database_config['port'], 
                                     database=database_config['database'], 
                                     auth_plugin=database_config['auth_plugin'])
        cursor = db.cursor()
        use_query = "USE Reddit"
        cursor.execute(use_query)

        # Loop through all posts retrieved from cmd line arguments. For each post iterate over all comments.
        # Store all of the data in database

        i_p = 0  # So I can make the process verbose
        i_c = 0  # So I can make the process verbose
        for submission in submissions:
            if i_p % 5 == 0:
                print(f"Completed {i_p} posts")
            i_p += 1

            try:
                submission.comments.replace_more(limit=None)
                for comment in submission.comments.list():

                    if comment.author == "None":
                        continue

                    c_info = get_comment_info(comment)
                    to_add = [c_info['body'], c_info['author'], c_info['score'], c_info['subreddit'], c_info['datetime']]
                    insert_query = """
                                    INSERT IGNORE INTO Comment 
                                    VALUES (DEFAULT, %s, %s, %s, %s, %s)
                                    """
                    cursor.execute(insert_query, to_add)
                    db.commit()
                    if i_c % 50 == 0 and i_c != 0:
                        print(f'Completed {i_c} comments')
                    i_c += 1

            except AttributeError:
                continue


    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))

    finally:
        if db.is_connected():
            db.close()
            print("MySQL connection is closed")

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    reddit_bot = create_reddit_bot(config, praw)

    # Cmd line argument for desired subreddit
    submissions = reddit_bot.subreddit(sys.argv[1]).hot(limit=1000)
    
    connect_database(config, submissions)

    #Create object 


if __name__ == "__main__":
    main()
    
