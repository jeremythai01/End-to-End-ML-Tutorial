#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import warnings
import joblib
from pandas.core.frame import DataFrame
from sklearn.feature_extraction.text import TfidfVectorizer
from functools import reduce
from sklearn.decomposition import PCA


class SentimentAnalyzer():
    """Sentiment analysis machine learning model to predict the sentiment of  

    Reddit comments.
    """
    def __init__(self):
        
        print("importing model, vectorizer and pca estimators...")

        # Filter incoming warnings when importing model, vectorizer and pca estimators 
        warnings.filterwarnings(action="ignore", message="Trying to unpickle estimator")

        self._model = joblib.load('./artifacts/sentiment_svm_model.pkl')
        self._vectorizer = joblib.load('./artifacts/Tfidf_Vectorizer_v1.pkl')
        self._pca = joblib.load('./artifacts/pca_v1.pkl')


    def predict_sentiment(self, df_comments: DataFrame):
        """Preprocess comments and predict sentiment for each of them.

        Parameters
        ----------
        df : Dataframe 
             The comments to be preprocessed and predicted.
        
        Returns
        -------
        df : dataframe with new sentiment column
        """
        applied_vectorization_comments = self._vectorizer.transform(df_comments['body']).toarray()
        applied_pca_comments = self._pca.transform(applied_vectorization_comments)

        #0 = negative, #1 = positive
        prediction_proba = self._model.predict_proba(applied_pca_comments) 
        prediction_score = [reduce(lambda x, y: round(y - x, 4), row) for row in prediction_proba]
    
        df_comments['score'] = prediction_score

        # Drop body column
        df_comments.drop(columns=['body'], inplace=True)
        
        return df_comments


    def vectorize_training(self, df: DataFrame):

        vectorizer = TfidfVectorizer()
        pca = PCA(n_components=150) 
        vectorized_text = vectorizer.fit_transform(df['cleaned text'])
        vectorized_text = pca.fit_transform(vectorized_text) # fits columns to 150
        
        #Save vectorizer
        pkl_filename = "Tfidf_Vectorizer_v1.pkl"
        with open('./ml/artifacts/'+ pkl_filename, 'wb') as file:
            pickle.dump(vectorizer, file)
        
        #Save pca
        pkl_filename = "pca_v1.pkl"
        with open('./ml/artifacts/'+pkl_filename, 'wb') as file:
            pickle.dump(pca, file)

        return vectorized_text