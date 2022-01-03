from datetime import datetime, timezone
import boto3
from decouple import config

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