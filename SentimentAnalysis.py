import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 


class SentimentAnalysis():

    def __init__(self):
        self.__model = SentimentIntensityAnalyzer() 
        self.__stemmer = PorterStemmer() 
        self.__lemmatizer = WordNetLemmatizer()
        self.__tokenizer = RegexpTokenizer(r'\w+')

    def analyze_sentiment(self, submission_set):

        results = {'pos': 0, 'neg': 0, 'neu': 0}

        for submission in submission_set:
            clean_title = self.preprocess_text(submission.get_title())
            self.predict(clean_title, results)
            for comment in submission.get_comments():
                clean_text = self.preprocess_text(comment.get_body())
                self.predict(clean_text, results)
                
        return results
    

    def predict(self, text, results):

        score = self.__model.polarity_scores(text)
        if score['compound'] > 0.05:
            results['pos'] += 1
        elif score['compound'] < -0.05:
            results['neg'] += 1
        else:
            results['neu'] += 1


    def preprocess_text(self, text):

        text = str(text).lower().replace('{html}',"") 
    
        cleanr = re.compile('<.*?>')
        clean_text = re.sub(cleanr, '', text)

        rem_url = re.sub(r'http\S+', '', clean_text)
        rem_num = re.sub('[0-9]+', '', rem_url)

        tokens = self.__tokenizer.tokenize(rem_num)  
        filtered_words = [w for w in tokens if len(w) > 2 if not w in stopwords.words('english')]
        stem_words=[self.__stemmer.stem(w) for w in filtered_words]
        lemma_words=[self.__lemmatizer.lemmatize(w) for w in stem_words]

        return " ".join(filtered_words)
