import pandas as pd
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import pickle

class Preprocessing():

    def __init__(self):
        self.__stemmer = PorterStemmer() 
        self.__lemmatizer = WordNetLemmatizer()
        self.__tokenizer = RegexpTokenizer(r'\w+')
        self.__vectorizer = pickle.load(open('./src/ml/nlp_tools/Tfidf_Vectorizer.pkl','rb'))
        self.__pca = pickle.load(open('./src/ml/nlp_tools/pca.pkl','rb'))


               
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

            clean_body = " ".join(lemma_words)
            clean_body_list.append(clean_body)            
        
        df['cleaned body'] = clean_body_list

        return df

    def vectorize(self, df):

        vector = self.__vectorizer.transform(df['cleaned body']).toarray()
        vector = self.__pca.transform(vector)    # fits columns to 256 with minimal loss
        return vector