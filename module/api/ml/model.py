#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle
import warnings
import wget
from functools import reduce
from ml.preprocessing import Preprocessing


class SentimentAnalysisModel():
    """Sentiment analysis machine learning model to predict the sentiment of  

    Reddit comments.
    """
    def __init__(self):

        model_name = "sentiment_svm_model.pkl"
        model_path = f'./ml/models/{model_name}'

        if model_name not in os.listdir('./ml/models/'):
            print(f'downloading the trained model {model_name}')
            wget.download(
                "https://github.com/jeremythai01/End-to-End-ML/releases/download/model/sentiment_svm_model.pkl",
                out=model_path
            )
        else:
            print('model already saved to /ml/models')
        
        # Filter incoming warnings when importing model
        warnings.filterwarnings(action="ignore", message="Trying to unpickle estimator ")
        self.__model = pickle.load(open('./ml/models/sentiment_svm_model.pkl','rb'))
        self.__preprocessing = Preprocessing()


    def predict_sentiment(self, df):
        """Preprocess comments and predict sentiment for each of them.

        Parameters
        ----------
        df : Dataframe 
             The comments to be preprocessed and predicted.
        
        Returns
        -------
        df : dataframe with new sentiment column
        """
        df = self.__preprocessing.preprocess_text(df)
        data_vector = self.__preprocessing.vectorize(df)
        
        #0 = negative, #1 = positive
        prediction_proba = self.__model.predict_proba(data_vector) 
        prediction_score = [reduce(lambda x, y: round(y - x, 4), row) for row in prediction_proba]
    
        df['sentiment'] = prediction_score

        df.drop(columns=['cleaned text'], inplace=True)
        
        return df