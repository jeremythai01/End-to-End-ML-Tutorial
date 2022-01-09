import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer


class TextPreprocessor():
    """Text preprocessor class to clean Reddit comments and prepare it for 
    
    NLP model prediction.
    """
    def __init__(self):
        self.__stemmer = PorterStemmer() 
        self.__lemmatizer = WordNetLemmatizer()
        self.__tokenizer = RegexpTokenizer(r'\w+')
        self.__stopwords = stopwords.words('english')

    def preprocess_text(self, text: str):
        """Preprocess comments with different techniques to transform them 
        
        into a more predictable form for the model.

        Parameters
        ----------
        text : string 
               The comment to be preprocessed.
        
        Returns
        -------
        text : preprocessed text
        """

        # Lowercasing, removing digits and non alphabetic characters
        text = str(text).lower().replace('{html}',"") 
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
                
        return clean_text