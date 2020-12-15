import praw
import config
import mysql.connector

def get_post_info(pos):
    """This method will acquire the needed info for a reddit post"""
    return {
        'title': pos.title, 'author': str(pos.author), 'upvote_ratio': pos.upvote_ratio, 'id': pos.id
    }


def get_comment_info(com):
    """This method will acquire the needed info for reddit comments"""
    return {
        'body': com.body, 'comment_id': com.id, 'parent_id': com.parent_id,
        'link_id': com.link_id, 'author': str(com.author), 'score': com.score
    }


def connect_database(config):
    try:
        database_config = config['database_config']
        # Connect to the database
        db = mysql.connector.connect(host=database_config['host'], 
                                     user=database_config['user'], 
                                     port=database_config['port'], 
                                     password=database_config['password'],
                                     database=database_config['database'], 
                                     auth_plugin=database_config['auth_plugin'])
        cursor = db.cursor()
        use_query = "USE Reddit"
        cursor.execute(use_query)

        # Loop through all posts retrieved from cmd line arguments. For each post iterate over all comments.
        # Store all of the data in database

        i_p = 0  # So I can make the process verbose
        i_c = 0  # So I can make the process verbose
        for post in sub_filter:
            info = get_post_info(post)
            to_add = [info['title'], info['author'], info['upvote_ratio'], info['id'], sub_class]
            insert_query = """
                                    INSERT IGNORE INTO Posts 
                                    VALUES (DEFAULT, %s, %s, %s, %s, %s)
                                    """
            cursor.execute(insert_query, to_add)
            db.commit()
            if i_p % 5 == 0:
                print(f"Completed {i_p} posts")
            i_p += 1

            try:
                for comment in post.comments:
                    c_info = get_comment_info(comment)
                    to_add = [c_info['body'], c_info['comment_id'], c_info['parent_id'], c_info['link_id'],
                            c_info['author'], c_info['score'], sub_class]
                    insert_query = """
                                    INSERT IGNORE INTO Comments 
                                    VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s)
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
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")