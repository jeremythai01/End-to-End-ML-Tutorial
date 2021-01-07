from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import pandas as pd
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer 
import re

class SentimentAnalysis():

    def __init__(self):
        self.__model = SentimentIntensityAnalyzer() 
        self.__stemmer = PorterStemmer() 
        self.__lemmatizer = WordNetLemmatizer()
        self.__tokenizer = RegexpTokenizer(r'\w+')

    def sentiment_score(self, df):

        df_copy = df.copy()

        clean_df = self.__preprocess_text(df_copy)

        return self.__predict(clean_df)
        

    def __predict(self, clean_df):


        clean_df['sentiment'] = None

        for i in range(len(clean_df.axes[0])):

            prediction_score = self.__model.polarity_scores(clean_df['body'][i])
            clean_df['sentiment'][i] = prediction_score['compound']
       
        return clean_df

               
    def __preprocess_text(self, df):

        for i in range(len(df.axes[0])):

            text = str(df['body'][i]).lower().replace('{html}',"") 
            cleanr = re.compile('<.*?>')
            clean_text = re.sub(cleanr, '', text)

            rem_url = re.sub(r'http\S+', '', clean_text)
            rem_num = re.sub('[0-9]+', '', rem_url)

            tokens = self.__tokenizer.tokenize(rem_num)  
            filtered_words = [w for w in tokens if not w in stopwords.words('english')]
            stem_words=[self.__stemmer.stem(w) for w in filtered_words]
            lemma_words=[self.__lemmatizer.lemmatize(w) for w in stem_words]

            df['body'][i] =  " ".join(lemma_words)

        return df
        
