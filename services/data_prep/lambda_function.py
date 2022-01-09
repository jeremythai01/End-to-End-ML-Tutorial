import pandas as pd
import json
from helpers import *
from utils.warehouse_connection import WarehouseConnection

def preprocess_comments(data):
    df_comments = pd.DataFrame(json.loads(data))
    return df_comments.pipe(drop_unpopular_comments) \
                      .pipe(drop_irrelevant_posts)   \
                      .pipe(convert_date_time_zone)  \
                      .pipe(preprocess_comment_body)

    
def lambda_handler(event, context):
    
    raw_data = read_comments_file_s3()

    print("processing..")

    df_comments = preprocess_comments(raw_data)
    
    comments_data = df_comments.to_dict('r') # store dicts in array

    print("querying..")

    WarehouseConnection.getInstance().query(get_comment_insert_query(), comments_data)


if __name__ == '__main__':
    lambda_handler(None, None)