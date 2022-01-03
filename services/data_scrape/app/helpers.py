import boto3
import json
from datetime import datetime
from decouple import config
from typing import Dict, List

def get_dt_now():

        dt_now = datetime.now()

        return (
            dt_now.strftime("%Y-%m-%d")
            + "_"
            + dt_now.strftime("%H:%M:%S")
        )


def write_to_local(comments: List[Dict[str,str]]):
    location = "/tmp"
    filename = get_dt_now() + ".json"
    local_filepath = location + "/" + filename

    # Write to local 
    with open(local_filepath, "w") as jsonFile:
            json.dump(comments, jsonFile)

    return local_filepath, filename


def upload_to_s3(local_filepath, filename):

    s3 = boto3.client('s3', aws_access_key_id=config('AWS_ACCESS_KEY_ID'), 
                    aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'))

    # Filename - File to upload
    # Bucket - Bucket to upload to (the top level directory under AWS S3)
    # Key - S3 object name (can contain subdirectories). If not specified then file_name is used
    s3.upload_file(Filename=local_filepath, Bucket=config('AWS_S3_BUCKET'), Key=filename)