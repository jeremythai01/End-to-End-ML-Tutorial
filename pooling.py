import os

import pymysql
from DBUtils.PooledDB import PooledDB
from dotenv import load_dotenv

MYSQL_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "db": "test_db",
    "password": "password",
    "user": "redowan",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": True,
}


POOL_CONFIG = {
    # Modules using linked databases
    "creator": pymysql,
    # Maximum connections allowed for connection pool,
    # 0 and None Indicates unlimited connections
    "maxconnections": 6,
    # At least idle links created in the link pool during initialization,
    # 0 means not to create
    "mincached": 2,
    # The most idle links in the link pool,
    # 0 and None No restriction
    "maxcached": 5,
    # The maximum number of links shared in the link pool,
    # 0 and None Represents all shares.
    # PS: It's useless because pymysql and MySQLdb Equal module threadsafety
    # All are 1, no matter how many values are set,_maxcached Always 0,
    # so always all links are shared.
    "maxshared": 3,
    # If there is no connection available in the connection pool,
    # whether to block waiting. True，Waiting;
    # False，Don't wait and report an error
    "blocking": True,
    # The maximum number of times a link is reused,
    # None Indicates unlimited
    "maxusage": None,
    # List of commands executed before starting a session.
    # Such as:["set datestyle to ...", "set time zone ..."]
    "setsession": [],
    # ping MySQL Server, check whether the service is available.
    # # For example: 0 = None = never,
    # 1 = default = whenever it is requested,
    # 2 = when a cursor is created,
    # 4 = when a query is executed,
    # 7 = always
    "ping": 0,
}

POOL = PooledDB(**MYSQL_CONFIG, **POOL_CONFIG)


class SqlPooled:
    def __init__(self):
        self._connection = POOL.connection()
        self._cursor = self._connection.cursor()

    def fetch_one(self, sql, args):
        self._cursor.execute(sql, args)
        result = self._cursor.fetchone()
        return result

    def fetch_all(self, sql, args):
        self._cursor.execute(sql, args)
        result = self._cursor.fetchall()
        return result

    def __del__(self):
        self._connection.close()


# Using the class in a function that creates a table in the localdb
obj = SqlPooled()


def create_post_table():
    """Create a table named `test_db` in the `posts_data` db.
    Before running the function, make sure that this
    `posts_data` db has been created in a local
    sql db and that server is running."""

    sql = """
    CREATE TABLE test_db.post_table (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    page_id varchar(100) NULL,
    link varchar(500) NULL,
    likes varchar(100) NULL,
    post_id varchar(100) NULL,
    post_url varchar(500) NULL,
    `time` TIMESTAMP NULL,
    comments_num varchar(100) NULL

    )
    ENGINE=InnoDB
    DEFAULT CHARSET=utf8mb4;
    """

    try:
        result = obj.fetch_all(sql, None)
    except pymysql.InternalError:
        print("Table Exists!!")
        pass


if __name__ == "__main__":
    create_post_table()
