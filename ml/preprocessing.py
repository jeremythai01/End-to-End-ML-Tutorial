import pandas as pd
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
import re

class SentimentAnalysis():

    def __init__(self):
        self.__stemmer = PorterStemmer() 
        self.__lemmatizer = WordNetLemmatizer()
        self.__tokenizer = RegexpTokenizer(r'\w+')
        self.__vectorizer = TfidfVectorizer()
        self.__pca = PCA(n_components=256)


    def sentiment_score(self, df):

        df = self.__preprocess_text(df)

        return self.__predict(df)
        

    def __predict(self, df):

        sentiment_list = []


        for i in range(len(df.axes[0])):

            prediction_score = self.__model.polarity_scores(df['cleaned body'][i])

            sentiment_list.append(prediction_score['compound'])
            
        df['sentiment'] = sentiment_list

        df.drop(columns=['cleaned body'], inplace=True)
        
        return df

               
    def preprocess_text(self, df):

        clean_body_list = []

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

            clean_body_list.append(" ".join(lemma_words))

        clean_body_array = self.__vectorizer.fit_transform(clean_body_list).toarray()
        clean_body_array = self.__pca.fit_transform(clean_body_array)

        df['cleaned body'] = clean_body_array

        return df
        
