#! /usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2
from psycopg2.extras import RealDictCursor
from decouple import config


class WarehouseConnection:
    """Database connection singleton to make sure that only one connection is
    
    made with the database.
    """
    _instance = None

    @staticmethod 
    def getInstance():
        """Static access method."""
        if WarehouseConnection._instance == None:                                    
            WarehouseConnection()

        return WarehouseConnection._instance


    def __init__(self):
        """Virtually private constructor."""
        if WarehouseConnection._instance != None:
            raise Exception("This class is a singleton!")
        else:
            WarehouseConnection._instance = self
            WarehouseConnection._instance._db_connection = self._connect_database()
            WarehouseConnection._instance._db_cursor = self._db_connection.cursor()

    def _connect_database(self):
        """Connect to Postgres database.

        Returns
        -------
        connection : new database connection
        """
        
        try:
            connection = psycopg2.connect(host=config('WAREHOUSE_HOST'), 
                                    database=config('WAREHOUSE_DB'), 
                                    user=config('WAREHOUSE_USER'), 
                                    password=config('WAREHOUSE_PASSWORD'), 
                                    cursor_factory=RealDictCursor) # Give column names to values dict
            connection.autocommit = True
            print("Database connection was successful!")
        except Exception as error:
            print("Connecting to database failed")
            print("Error:", error)
            quit()
        
        return connection
        

    def fetch(self, query):
        self._instance._db_cursor.execute(query)
        comments = self._instance._db_cursor.fetchall()
        return comments

    