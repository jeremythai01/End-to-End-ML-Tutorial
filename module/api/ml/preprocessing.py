#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import re
import warnings
import pandas as pd
import nltk
nltk.download("stopwords")
nltk.download('wordnet')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler


class Preprocessing():
    """Preprocessing class to clean Reddit comments and prepare it for 
    
    NLP model prediction.
    """
    def __init__(self):
        self.__stemmer = PorterStemmer() 
        self.__lemmatizer = WordNetLemmatizer()
        self.__tokenizer = RegexpTokenizer(r'\w+')
        # Filter incoming warnings when importing vectorizer and pca estimator
        warnings.filterwarnings(action="ignore", message="Trying to unpickle estimator ")
        self.__vectorizer = pickle.load(open('./ml/nlp_tools/Tfidf_Vectorizer.pkl','rb'))
        self.__pca = pickle.load(open('./ml/nlp_tools/pca.pkl','rb'))
        self.__stopwords = stopwords.words('english')


    def preprocess_text(self, df):
        """Preprocess comments with different techniques to transform them 
        
        into a more predictable form for the model.

        Parameters
        ----------
        df : Dataframe 
             The comments to be preprocessed.
        
        Returns
        -------
        df : dataframe with new cleaned text column
        """
        clean_text_list = []

        for i in range(len(df.axes[0])):

            # Lowercasing, removing digits and non alphabetic characters
            text = str(df['text'][i]).lower().replace('{html}',"") 
            cleanr = re.compile('<.*?>')
            clean_text = re.sub(cleanr, '', text)
            rem_url = re.sub(r'http\S+', '', clean_text)
            rem_num = re.sub('[0-9]+', '', rem_url)

            #Tokenization
            tokens = self.__tokenizer.tokenize(rem_num)  

            #Removing stop words
            filtered_words = [w for w in tokens if not w in self.__stopwords]

            #Stemming
            stem_words=[self.__stemmer.stem(w) for w in filtered_words]

            #Lemming
            lemma_words=[self.__lemmatizer.lemmatize(w) for w in stem_words]

            clean_text = " ".join(lemma_words)
            clean_text_list.append(clean_text)            
        
        df['cleaned text'] = clean_text_list

        return df

    def vectorize(self, df):
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