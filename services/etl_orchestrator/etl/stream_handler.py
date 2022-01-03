#! /usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Tuple
from pandas.core.frame import DataFrame
from etl.database_connection import DBConnection


class StreamHandler():
    """Stream handler to perform data retrieval and streaming with the 
    
    database.
    """
    def __init__(self):
        self.__db_connection = DBConnection.getInstance()


    def stream_to_database(self, df: DataFrame):
        """Stream transformed data to database.

        Parameters
        ----------
        df : Dataframe
             The dataframe of transformed Reddit comments
        """
        i_c = 0
        for i in range(len(df.axes[0])): # Iterate row by row
            
            try:
                to_add = [df['subreddit'][i], 
                          df['author'][i], 
                          df['text'][i], 
                          df['date'][i], 
                          float(df['sentiment'][i])
                          ]
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


    def retrieve_data(self, size: int):
        """Retrieve specified data from database.

        Parameters
        ----------
        size : integer 
               The max size of row to be retrieved.

        Returns
        -------
        sentiment_data : list of tuples of sentiment scores and dates
        """
        insert_query = "SELECT date, sentiment FROM Comment ORDER BY date DESC LIMIT " + str(size)

        self.__db_connection.query(insert_query)

        sentiment_data = self.__db_connection.fetchall()

        return sentiment_data


    def serialize(self, row: Tuple):
        """Seralize specified row fetched from database.

        Parameters
        ----------
        row : tuple 
              The sentiment score and date.

        Returns
        -------
        sentiment_data_serialized : dict of sentiment score and date
        """
        sentiment_data_serialized =  {'date' : row[0], 'sentiment' : row[1]}

        return sentiment_data_serialized


    def close_db_connection(self):
        """Close connection with the database."""
        self.__db_connection.close()