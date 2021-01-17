import os
import pickle
import wget
from ml.preprocessing import Preprocessing
from functools import reduce
import warnings

class SentimentAnalysisModel():

    def __init__(self):

        model_name = "sentiment_svm_model.pkl"
        model_path = f'./ml/models/{model_name}'

        if model_name not in os.listdir('./ml/models/'):
            print(f'downloading the trained model {model_name}')
            wget.download(
                "https://github.com/jeremythai01/End-to-End-ML/releases/download/model/sentiment_svm_model.pkl",
                out=model_path
            )
        else:
            print('model already saved to /ml/models')
            
        warnings.filterwarnings(action="ignore", message="Trying to unpickle estimator ")
        self.__model = pickle.load(open('./ml/models/sentiment_svm_model.pkl','rb'))
        self.__preprocessing = Preprocessing()


    def predict_sentiment(self, df):

        df = self.__preprocessing.preprocess_text(df)
        data_vector = self.__preprocessing.vectorize(df)
        prediction_proba = self.__model.predict_proba(data_vector) #0 = negative, #1 = positive
        prediction_score = [reduce(lambda x, y: round(y - x, 4), row) for row in prediction_proba]
    
        df['sentiment'] = prediction_score
        

        df.drop(columns=['cleaned body'], inplace=True)
        
        return df