#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import re
import warnings
import nltk
from pandas.core.frame import DataFrame
nltk.download("stopwords")
nltk.download('wordnet')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer


class TextCleaner():
    """Text cleaner class to clean Reddit comments and prepare it for 
    
    NLP model prediction.
    """
    def __init__(self):
        self.__stemmer = PorterStemmer() 
        self.__lemmatizer = WordNetLemmatizer()
        self.__tokenizer = RegexpTokenizer(r'\w+')
        self.__stopwords = stopwords.words('english')


    def clean_text(self, df: DataFrame):
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