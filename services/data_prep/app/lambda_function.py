import pandas as pd
import json
from helpers import *

def preprocess_comment(data):
    df_comments = pd.DataFrame(json.loads(data))
    df_comments.pipe(drop_unpopular_comments) \
                .pipe(drop_irrelevant_posts) \
                .pipe(convert_date_time_zone) \
                .pipe(upper_case_is_mod) \
                .pipe(upper_case_is_gold) \
                .pipe(preprocess_comment_body) 

def lambda_handler():
    
    data = read_comments_file_s3()
    preprocess_comment(data)
    


if __name__ == '__main__':
    lambda_handler()