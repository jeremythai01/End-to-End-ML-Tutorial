import mysql.connector
from decouple import config


class DBConnectionSingleton:
    """Database connection singleton to make sure that only one connection is
    
    made with the database.
    """
    __instance = None

    @staticmethod 
    def getInstance():
        """Static access method."""
        if DBConnectionSingleton.__instance == None:                                    
            DBConnectionSingleton()

        return DBConnectionSingleton.__instance


    def __init__(self):
        """Virtually private constructor."""
        if DBConnectionSingleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DBConnectionSingleton.__instance = self
            DBConnectionSingleton.__instance.__db_connection = self.__connect_database()
            DBConnectionSingleton.__instance.__db_cursor = self.__db_connection.cursor()
            self.query("USE Reddit")    


    def __connect_database(self):
        """Connect to MySQL database.

        Returns
        -------
        connection : new database connection
        """
        try:
            connection = mysql.connector.connect(host=config('MYSQL_HOST'), 
                                            user=config('MYSQL_USER'), 
                                            password=config('MYSQL_ROOT_PASSWORD'),
                                            port=config('MYSQL_PORT'), 
                                            database=config('MYSQL_DB'))

        except mysql.connector.Error as error:
            print("Failed to insert record into table {}".format(error))
            quit()
        
        return connection


    def close(self):
        """Close connection with the database."""
        self.__db_connection.close()
        print("MySQL connection is closed")     


    def query(self, query, params=None):
        """Execute an SQL query.

        Parameters
        ----------
        query :  string 
                 The request for the database.

        params : list of values, default=None
                 The values to be targeted by the query.
        """
        self.__db_cursor.execute(query, params)
        

    def commit(self):
        """Commit the current transaction."""
        self.__db_connection.commit()


    def fetchall(self):
        """Fetch all rows of a query result set.

        Returns
        -------
        rows : rows of a query result set
        """
        rows = self.__db_cursor.fetchall()

        return rows