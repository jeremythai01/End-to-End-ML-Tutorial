from decouple import config

       
def get_sentiment_select_query():
        return '''
            SELECT s.score, c.date
            FROM Reddit.Comment c INNER JOIN Reddit.Sentiment s ON c.id = s.idComment
            ORDER BY c.date;
        '''