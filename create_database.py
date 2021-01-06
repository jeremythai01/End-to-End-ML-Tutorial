import mysql.connector
import configparser

def main():

        config = configparser.ConfigParser()
        config.read('config.ini')
        database_config = config['database_config']
        db = mysql.connector.connect(host=database_config['host'], 
                                        user=database_config['user'], 
                                        port=database_config['port'], 
                                        password=database_config['password'],
                                        database=database_config['database'], 
                                        auth_plugin=database_config['auth_plugin'])
        cursor = db.cursor()
        cursor.execute("""
                        CREATE TABLE Comment (
                                id_num MEDIUMINT NOT NULL AUTO_INCREMENT, 
                                subreddit VARCHAR(20),
                                author VARCHAR(20), 
                                body VARCHAR(250) UNIQUE, 
                                date VARCHAR(20),
                                PRIMARY KEY (id_num))
                        """)
        db.commit() 


if __name__ == "__main__":
        main()