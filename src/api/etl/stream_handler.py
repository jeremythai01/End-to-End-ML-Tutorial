from etl.database_connection import DBConnectionSingleton

class StreamHandler():

    def __init__(self):
        self.__db_connection = db_connection = DBConnectionSingleton.getInstance()

    def stream_to_database(self, df):

        i_c = 0
        for i in range(len(df.axes[0])):
            
            try:
                to_add = [df['subreddit'][i], df['author'][i], df['body'][i], df['date'][i], float(df['sentiment'][i])]
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


    def load_data(self, size):
        insert_query = "SELECT date, sentiment FROM Comment ORDER BY date DESC LIMIT " + str(size)

        self.__db_connection.query(insert_query)

        data = self.__db_connection.fetchall()

        return data

    def serialize(self, row):
        return {
            'date': row[0],
            'sentiment' : row[1]
        }

    def close_db_connection(self):
        self.__db_connection.close()