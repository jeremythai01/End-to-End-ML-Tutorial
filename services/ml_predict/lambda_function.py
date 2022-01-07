
from sentiment_analyzer import SentimentAnalyzer
from warehouse_connection import WarehouseConnection
from helpers import *
import pandas as pd


def lambda_handler(event, context):

    warehouse_connection = WarehouseConnection.getInstance()
    sentiment_analyzer = SentimentAnalyzer()

    data = warehouse_connection.fetch(get_comment_select_query())

    df_comments = pd.DataFrame.from_records(dict(row) for row in data)

    df_pred = sentiment_analyzer.predict_sentiment(df_comments)

    pred_data = df_pred.to_dict('r') # store dicts in array

    print("querying..")

    warehouse_connection.query(get_sentiment_insert_query(), pred_data)

if __name__ == '__main__':
    lambda_handler(None, None)