import boto3
from decouple import config
from datetime import datetime, timezone
from text_preprocessor import TextPreprocessor


def drop_unpopular_comments(df):
    MIN_SCORE = 10
    return df[df['score'].astype(int) >= MIN_SCORE]


def drop_irrelevant_posts(df):
    excluded_submission_keywords = ['Thread', 'Daily Discussion', 'Rate My Portfolio']
    pattern = '|'.join(excluded_submission_keywords)
    return df[~df['post'].str.contains(pattern)]


def convert_time_zone(date):
    utc_datetime = datetime.utcfromtimestamp(float(date))
    local_datetime = utc_datetime.replace(tzinfo=timezone.utc).astimezone(tz=None)
    local_datetime = local_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return local_datetime


def convert_date_time_zone(df):
    df['date'] = df['date'].apply(convert_time_zone)
    return df


def upper_case_is_mod(df):
    df['author_is_mod'] = df['author_is_mod'].apply(lambda x: str(x).upper())
    return df


def upper_case_is_gold(df):
    df['author_is_gold'] = df['author_is_gold'].apply(lambda x: str(x).upper())
    return df


def preprocess_comment_body(df):
    text_preprocessor = TextPreprocessor()
    df['body'] = df['body'].apply(text_preprocessor.preprocess_text)
    return df


def read_comments_file_s3():
       
       s3 = boto3.client('s3', aws_access_key_id=config('AWS_ACCESS_KEY_ID'), 
                    aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'))

       BUCKET = config('AWS_S3_BUCKET')

       # Lambda function to get last modified time
       get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))

       # Get all objects
       objs = s3.list_objects_v2(Bucket=BUCKET)['Contents']

       # Find last modified/added object key
       last_added = [obj['Key'] for obj in sorted(objs, key=get_last_modified)][-1]
       

       result = s3.get_object(Bucket=BUCKET, Key=last_added) 
       result = result["Body"].read().decode('utf-8')            
       
       return result