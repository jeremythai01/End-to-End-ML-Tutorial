import unittest
import pandas as pd
from services.ml_predict.sentiment_analyzer import SentimentAnalyzer

class TestSentimentAnalyzer(unittest.TestCase):

    def setUp(self):
        self.model = SentimentAnalyzer()

    def test_predict_sentiment(self):   
        df = pd.DataFrame()
        text = ["This is a test sentence", "another one"]
        df['body'] = text
        
        result_df = self.model.predict_sentiment(df)
        scores = result_df['score'].tolist()

        self.assertFalse('body' in result_df.columns)
        self.assertTrue('score' in result_df.columns)
        self.assertTrue(str(score)[::-1].find('.') > 2 for score in scores)