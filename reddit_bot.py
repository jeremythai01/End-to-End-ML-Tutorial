class Singleton:

    __instance = None
    config = configparser.ConfigParser()
    config.read('config.ini')

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if Singleton.__instance == None:
            Singleton()

        return Singleton.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Singleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Singleton.__instance = self

        def create_reddit_bot(config, praw):
            #Create reddit instance
            
            bot_config = config['bot_config']
            reddit_bot = praw.Reddit(username=bot_config['username'],
                                    password=bot_config['password'],
                                    client_id=bot_config['client_id'],
                                    client_secret=bot_config['client_secret'],
                                    user_agent=bot_config['user_agent'])
            return reddit_bot


    