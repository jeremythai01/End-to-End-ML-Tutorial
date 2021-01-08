import pandas as pd
import re

class SentimentAnalysisSVM():

    def __init__(self, preprocessing):

        self.__model = None 
        self.__preprocessing = preprocessing


    def predict_sentiment(self, df):

        df = self.__preprocessing.preprocess_text(df)

        sentiment_list = []

        for i in range(len(df.axes[0])):

            prediction_score = self.__model.predict(df['cleaned body'][i])

            sentiment_list.append(prediction_score['compound'])
            
        df['sentiment'] = sentiment_list

        df.drop(columns=['cleaned body'], inplace=True)
        
        return df