#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle
import warnings
from pandas.core.frame import DataFrame
from sklearn.feature_extraction.text import TfidfVectorizer
import wget
from functools import reduce
from sklearn.decomposition import PCA


class SentimentAnalyzer():
    """Sentiment analysis machine learning model to predict the sentiment of  

    Reddit comments.
    """
    def __init__(self):

        model_name = "sentiment_svm_model.pkl"
        model_path = f'./ml/artifacts/{model_name}'

        if model_name not in os.listdir('./ml/artifacts/'):
            print(f'downloading the trained model {model_name}')
            wget.download(
                "https://github.com/jeremythai01/End-to-End-ML/releases/download/model/sentiment_svm_model.pkl",
                out=model_path
            )
        else:
            print('model already saved to /ml/artifacts')
        
        # Filter incoming warnings when importing model, vectorizer and pca estimators 
        warnings.filterwarnings(action="ignore", message="Trying to unpickle estimator ")
        self._model = pickle.load(open('./ml/artifacts/sentiment_svm_model.pkl','rb'))
        self.__vectorizer = pickle.load(open('./ml/artifacts/Tfidf_Vectorizer_v1.pkl','rb'))
        self.__pca = pickle.load(open('./ml/artifacts/pca_v1.pkl','rb'))


    def vectorize(self, df: DataFrame):
        """Convert cleaned comments to a matrix of TF-IDF numerical features.

        Parameters
        ----------
        df : Dataframe 
             The comments to be vectorized.
        
        Returns
        -------
        vectorized_text : 2D list of features to feed to model
        """
        vectorized_text = self.__vectorizer.transform(df['cleaned text']).toarray()
        vectorized_text = self.__pca.transform(vectorized_text)

        return vectorized_text


    def vectorize_training(self, df: DataFrame):

        vectorizer = TfidfVectorizer()
        pca = PCA(n_components=150) 
        vectorized_text = vectorizer.fit_transform(df['cleaned text']).toarray()
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



    def predict_sentiment(self, df: DataFrame):
        """Preprocess comments and predict sentiment for each of them.

        Parameters
        ----------
        df : Dataframe 
             The comments to be preprocessed and predicted.
        
        Returns
        -------
        df : dataframe with new sentiment column
        """
        data_vector = self.vectorize(df)
        
        #0 = negative, #1 = positive
        prediction_proba = self._model.predict_proba(data_vector) 
        prediction_score = [reduce(lambda x, y: round(y - x, 4), row) for row in prediction_proba]
    
        df['sentiment'] = prediction_score

        df.drop(columns=['cleaned text'], inplace=True)
        
        return df