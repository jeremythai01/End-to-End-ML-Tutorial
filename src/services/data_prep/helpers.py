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


def _convert_time_zone(date):
    utc_datetime = datetime.utcfromtimestamp(float(date))
    local_datetime = utc_datetime.replace(tzinfo=timezone.utc).astimezone(tz=None)
    local_datetime = local_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return local_datetime


def convert_date_time_zone(df):
    df['date'] = df['date'].apply(_convert_time_zone)
    return df


def preprocess_comment_body(df):
    text_preprocessor = TextPreprocessor()
    df['body'] = df['body'].apply(text_preprocessor.preprocess_text)
    return df


def read_comments_file_s3():
       
       s3 = boto3.client('s3', region_name=config('AWS_DEFAULT_REGION'),
                    aws_access_key_id=config('AWS_ACCESS_KEY_ID'), 
                    aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
                    aws_session_token=config('AWS_SESSION_TOKEN'))

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

       
def get_comment_insert_query():
        return '''
        INSERT INTO Reddit.Comment (
            post,
            author,
            authorCommentKarma,
            authorLinkKarma,
            isAuthorMod,
            isAuthorGold,
            idComment,
            body,
            score,
            "date"
        )
        VALUES (
            %(post)s,
            %(author)s,
            %(author_comment_karma)s,
            %(author_link_karma)s,
            %(author_is_mod)s,
            %(author_is_gold)s,
            %(comment_id)s,
            %(body)s,
            %(score)s,
            %(date)s
        )
        -- Dont insert duplicates
        ON CONFLICT (idComment) DO NOTHING; 
        '''