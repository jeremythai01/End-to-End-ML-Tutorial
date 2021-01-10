import mysql.connector
from configparser import ConfigParser
import os
def main():

        config = ConfigParser()
        path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
        config.read(os.path.join(path, 'database_config.ini'))
        database_config = config['database_config']

        try:
            # Connect to the database
            db = mysql.connector.connect(host=database_config['HOST'], 
                                        user=database_config['MYSQL_USER'], 
                                        password=database_config['MYSQL_PASSWORD'],
                                        port=database_config['MYSQL_PORT'], 
                                        database=database_config['MYSQL_DB'], 
                                        auth_plugin=database_config['MYSQL_AUTH_PLUGIN'])

        except mysql.connector.Error as error:
            print("Failed to insert record into Laptop table {}".format(error))
            quit()

        cursor = db.cursor()


        cursor.execute("USE Reddit")
        cursor.execute("DROP TABLE Comment")
        cursor.execute("""
                        CREATE TABLE Comment (
                                id_num MEDIUMINT NOT NULL AUTO_INCREMENT, 
                                subreddit VARCHAR(20),
                                author VARCHAR(20), 
                                body VARCHAR(250) UNIQUE, 
                                date VARCHAR(20),
                                sentiment FLOAT(4),
                                PRIMARY KEY (id_num))
                        """)
        db.commit() 


if __name__ == "__main__":
        main()