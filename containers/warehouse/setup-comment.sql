DROP TABLE IF EXISTS Reddit.Comment;
DROP SCHEMA IF EXISTS Reddit;

CREATE SCHEMA Reddit;

CREATE TABLE Reddit.Comment (
    id SERIAL PRIMARY KEY,
    post VARCHAR(200) NOT NULL,
    author VARCHAR(200) NOT NULL,
    authorCommentKarma NUMERIC(10) NOT NULL,
    authorLinkKarma NUMERIC(10) NOT NULL,
    isAuthorMod BOOL NOT NULL,
    isAuthorGold BOOL NOT NULL,
    commentId VARCHAR(200) NOT NULL UNIQUE,
    body VARCHAR(1000) NOT NULL,
    score NUMERIC(10) NOT NULL,
    "date" DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);