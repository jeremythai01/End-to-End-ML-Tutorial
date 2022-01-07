def get_comment_select_query():
        return '''
            SELECT id, body
            FROM Reddit.Comment
            ORDER BY id
        '''

def get_sentiment_insert_query():
        return '''
        INSERT INTO Reddit.Sentiment (
            idComment,
            score
        )
        VALUES (
            %(id)s,
            %(score)s
        )
        -- Dont insert duplicates
        ON CONFLICT (idComment) DO NOTHING; 
        '''