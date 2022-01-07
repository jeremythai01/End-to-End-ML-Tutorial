DROP TABLE IF EXISTS Reddit.Comment;
DROP TABLE IF EXISTS Reddit.Sentiment;

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
    idComment VARCHAR(200) NOT NULL UNIQUE,
    body TEXT NOT NULL,
    score NUMERIC(10) NOT NULL,
    "date" DATE NOT NULL,
    created_at TIMESTAMP DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'EST')
);

CREATE TABLE Reddit.Sentiment(
    id SERIAL PRIMARY KEY,
    idComment integer NOT NULL UNIQUE,
    score DECIMAL(5,4) NOT NULL,
    created_at TIMESTAMP DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'EST'),
	FOREIGN KEY(idComment) REFERENCES Reddit.Comment(id)
);