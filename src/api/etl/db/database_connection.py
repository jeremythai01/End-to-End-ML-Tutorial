import mysql.connector
from decouple import config

class DBConnectionSingleton:

    __instance = None

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if DBConnectionSingleton.__instance == None:
            DBConnectionSingleton()

        return DBConnectionSingleton.__instance


    def __init__(self):
        """ Virtually private constructor. """
        if DBConnectionSingleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DBConnectionSingleton.__instance = self
            DBConnectionSingleton.__instance.__db_connection = self.__connect_database()
            DBConnectionSingleton.__instance.__db_cursor = self.__db_connection.cursor()
            self.query("USE Reddit")

    def close(self):

        self.__db_connection.close()
        print("MySQL connection is closed")         


    def __connect_database(self):
          
        try:
            # Connect to the database
            database = mysql.connector.connect(host=config('MYSQL_HOST'), 
                                            user=config('MYSQL_USER'), 
                                            password=config('MYSQL_ROOT_PASSWORD'),
                                            port=int(str(config('MYSQL_PORT'))), 
                                            database=config('MYSQL_DB'))

        except mysql.connector.Error as error:
            print("Failed to insert record into Laptop table {}".format(error))
            quit()
        
        
        return database


    def query(self, query, params=None):
        self.__db_cursor.execute(query, params)
        

    def commit(self):
        self.__db_connection.commit()

    def fetchall(self):
        return self.__db_cursor.fetchall()