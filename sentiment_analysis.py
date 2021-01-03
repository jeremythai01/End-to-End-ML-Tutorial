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

    def sentiment_score(self, comment_set):

        score = 0

        for comment in comment_set:
            score += self.__predict(comment)

        return score
    


    def __predict(self, comment):

        clean_body = self.__preprocess_text(comment.get_body())
        score = self.__model.polarity_scores(clean_body)

        if score['compound'] >= 0.05: #Positive
            return comment.score
        elif score['compound'] <= -0.05: #Negative
            return -1 * comment.score
        else:
            return 0
       
    def __preprocess_text(self, text):

        text = str(text).lower().replace('{html}',"") 
    
        cleanr = re.compile('<.*?>')
        clean_text = re.sub(cleanr, '', text)

        rem_url = re.sub(r'http\S+', '', clean_text)
        rem_num = re.sub('[0-9]+', '', rem_url)

        tokens = self.__tokenizer.tokenize(text)  
        filtered_words = [w for w in tokens if not w in stopwords.words('english')]
        stem_words=[self.__stemmer.stem(w) for w in filtered_words]
        lemma_words=[self.__lemmatizer.lemmatize(w) for w in stem_words]

        return " ".join(lemma_words)
        
