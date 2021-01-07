class StreamHandler():

    def __init__(self, db_connection):
        self.__db_connection = db_connection

    def stream_to_database(self, df):

        i_c = 0
        for i in range(len(df.axes[0])):
            try:
                    to_add = [df['subreddit'][i], df['author'][i], df['body'][i], df['date'][i], df['sentiment'][i]]
                    insert_query = """
                                    INSERT IGNORE INTO Comment 
                                    VALUES (DEFAULT, %s, %s, %s, %s, %s)
                                    """
                    self.__db_connection.query(insert_query, to_add)
                    self.__db_connection.commit()
                    i_c += 1

            except AttributeError:
                continue

        print(f'Streamed {i_c} comments')

    def close_db_connection(self):
        self.__db_connection.close()




    





        



