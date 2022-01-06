import boto3
import json
from datetime import datetime, timezone
from decouple import config
from typing import Dict, List

def get_dt_now():

        dt_now = datetime.now()

        return (
            dt_now.strftime("%Y-%m-%d %H:%M:%S")
        )


def write_to_local(comments: List[Dict[str,str]]):
    location = "/tmp"
    filename = get_dt_now() + ".json"
    local_filepath = location + "/" + filename

    # Write to local 
    with open(local_filepath, "w") as jsonFile:
            json.dump(comments, jsonFile)

    return local_filepath, filename


# Ensure idempotency
def is_pipeline_idempotent():
    s3 = boto3.client('s3', aws_access_key_id=config('AWS_ACCESS_KEY_ID'), 
                    aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
                    aws_session_token=config('AWS_SESSION_TOKEN'))
    

    BUCKET = config('AWS_S3_BUCKET')

    # Lambda function to get last modified time
    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))

    # Get all objects
    try:
        objs = s3.list_objects_v2(Bucket=BUCKET)['Contents']
    except KeyError:
        return True # Empty S3 bucket

    # Find last modified/added object key
    last_added = [obj['LastModified'] for obj in sorted(objs, key=get_last_modified)][-1]

    datetime_now = datetime.now(timezone.utc)
    difference = (datetime_now - last_added).total_seconds()
    MIN_INTERVAL_SECONDS = 60
    return difference > MIN_INTERVAL_SECONDS


def upload_to_s3(local_filepath, filename):

    s3 = boto3.client('s3', aws_access_key_id=config('AWS_ACCESS_KEY_ID'), 
                    aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
                    aws_session_token=config('AWS_SESSION_TOKEN'))

    # Filename - File to upload
    # Bucket - Bucket to upload to (the top level directory under AWS S3)
    # Key - S3 object name (can contain subdirectories). If not specified then file_name is used
    s3.upload_file(Filename=local_filepath, Bucket=config('AWS_S3_BUCKET'), Key=filename)