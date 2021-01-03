from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer 
import re


class SentimentAnalysis():

    def __init__(self):
        self.__model = SentimentIntensityAnalyzer() 
        self.__stemmer = PorterStemmer() 
        self.__lemmatizer = WordNetLemmatizer()
        self.__tokenizer = RegexpTokenizer(r'\w+')

    def sentiment(self, comment_set):

        results = {'positive': 0, 'negative': 0, 'neutral': 0}

        for comment in comment_set:
            clean_title = self.__preprocess_text(comment.get_body())
            self.__predict(clean_title, results)

        return results
    

    def __predict(self, text, results):

        score = self.__model.polarity_scores(text)
        if score['compound'] > 0.05:
            results['positive'] += 1
        elif score['compound'] < -0.05:
            results['negative'] += 1
        else:
            results['neutral'] += 1

    def __preprocess_text(self, text):

        text = str(text).lower().replace('{html}',"") 
    
        cleanr = re.compile('<.*?>')
        clean_text = re.sub(cleanr, '', text)

        rem_url = re.sub(r'http\S+', '', clean_text)
        rem_num = re.sub('[0-9]+', '', rem_url)

        tokens = self.__tokenizer.tokenize(rem_num)  
        filtered_words = [w for w in tokens if len(w) > 2 if not w in stopwords.words('english')]
        stem_words=[self.__stemmer.stem(w) for w in filtered_words]
        lemma_words=[self.__lemmatizer.lemmatize(w) for w in stem_words]

        return " ".join(lemma_words)
