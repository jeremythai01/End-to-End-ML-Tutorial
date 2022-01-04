from reddit_bot import RedditBot
from helpers import write_to_local, upload_to_s3

def lambda_handler():
    LIMIT_POSTS = 3
    comments = RedditBot.getInstance().scrape_reddit("Stocks", LIMIT_POSTS)
    local_filepath, filename = write_to_local(comments)
    upload_to_s3(local_filepath, filename)


if __name__ == '__main__':
    lambda_handler()