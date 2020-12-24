from configparser import ConfigParser
import mysql.connector

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


    def __del__(self):
        self.__db_connection.close()
        print("MySQL connection is closed")         


    def __connect_database(self):
          
        config = ConfigParser()
        config.read('config.ini')
        database_config = config['database_config']

        try:
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


    def query(self, query, params=None):
        self.__db_cursor.execute(query, params)
        self.__commit()


    def __commit(self):
        self.__db_connection.commit()

   