import mysql.connector
import configparser


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
                        body VARCHAR(250) UNIQUE, 
                        comment_id VARCHAR(20), 
                        parent_id VARCHAR(20), 
                        link_id VARCHAR(150), 
                        author VARCHAR(150), 
                        score MEDIUMINT, 
                        class VARCHAR(20), 
                        PRIMARY KEY (id_num))
                """)
db.commit() 