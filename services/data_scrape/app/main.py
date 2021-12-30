from typing import Dict, List
from fastapi import FastAPI, status
from app.reddit_bot import RedditBot
from app.schemas import Comment

reddit_bot = RedditBot.getInstance()
app = FastAPI()

# Path operation
@app.get("/")
def root():
    return {"message": "Hello Data Scraper!"}


@app.get("/comments/{number_posts}")
def scrape_comments(number_posts: int):
    if number_posts <= 0:
        raise ValueError("number_posts argument must be positive value")

    number_posts = reddit_bot.scrape_reddit("Stocks", number_posts)

    return number_posts
    

@app.post("/comments", status_code=status.HTTP_201_CREATED)
def upload_comments(comments: List[Comment]):

    reddit_bot.upload_to_s3([comment.dict() for comment in comments])

    return comments

 