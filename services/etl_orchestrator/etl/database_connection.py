#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import psycopg2
from psycopg2.extras import RealDictCursor
from decouple import config


class DBConnection:
    """Database connection singleton to make sure that only one connection is
    
    made with the database.
    """
    _instance = None

    @staticmethod 
    def getInstance():
        """Static access method."""
        if DBConnection._instance == None:                                    
            DBConnection()

        return DBConnection._instance


    def __init__(self):
        """Virtually private constructor."""
        if DBConnection._instance != None:
            raise Exception("This class is a singleton!")
        else:
            DBConnection._instance = self
            DBConnection._instance._db_connection = self._connect_database()
            DBConnection._instance._db_cursor = self._db_connection.cursor()


    def _connect_database(self):
        """Connect to Postgres database.

        Returns
        -------
        connection : new database connection
        """
        while True: # break loop when connection is made
            try:
                connection = psycopg2.connect(host=config('POSTGRES_HOST'), 
                                        database=config('POSTGRES_DB'), 
                                        user=config('POSTGRES_USER'), 
                                        password=config('POSTGRES_PASSWORD'), 
                                        cursor_factory=RealDictCursor) # Give column names to values dict
                print("Database connection was successful!")
                break
            except Exception as error:
                print("Connecting to database failed")
                print("Error:", error)
                time.sleep(secs=2)
        
        return connection


    def close(self):
        """Close connection with the database."""
        self._instance._db_connection.close()
        print("MySQL connection is closed")     


    def query(self, query: str, params: list = None):
        """Execute an SQL query.

        Parameters
        ----------
        query :  string 
                 The request for the database.

        params : list of values, default=None
                 The values to be targeted by the query.
        """
        self._instance._db_cursor.execute(query, params)
        

    def commit(self):
        """Commit the current transaction."""
        self._instance._db_connection.commit()


    def fetchall(self):
        """Fetch all rows of a query result set.

        Returns
        -------
        rows : rows of a query result set
        """
        rows = self._instance._db_cursor.fetchall()

        return rows
