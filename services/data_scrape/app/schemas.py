from pydantic import BaseModel

class Comment(BaseModel):
    subreddit: str
    author: str
    text: str
    date: str 