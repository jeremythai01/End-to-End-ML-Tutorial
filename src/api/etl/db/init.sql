CREATE DATABASE Reddit;
use Reddit;

CREATE TABLE Comment (
    id_num MEDIUMINT NOT NULL AUTO_INCREMENT, 
    subreddit VARCHAR(20),
    author VARCHAR(20), 
    body VARCHAR(250) UNIQUE, 
    date DATETIME,
    sentiment FLOAT(4),
    PRIMARY KEY (id_num)
);
 