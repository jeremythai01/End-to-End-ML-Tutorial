from reddit_bot import RedditBot
from helpers import *

def lambda_handler(event, context):
    
    if not is_pipeline_idempotent():
        print("Interval time between pipeline runs is too small. Exiting..")
        return 

    LIMIT_POSTS = 3
    comments = RedditBot.getInstance().scrape_reddit("Stocks", LIMIT_POSTS)
    local_filepath, filename = write_to_local(comments)
    upload_to_s3(local_filepath, filename)

if __name__ == '__main__':
    lambda_handler(None, None)