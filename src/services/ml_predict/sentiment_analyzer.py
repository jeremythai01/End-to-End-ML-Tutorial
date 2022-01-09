from pandas.core.frame import DataFrame
from functools import reduce
from helpers import load_artifacts_from_s3

class SentimentAnalyzer():
    """Sentiment analysis machine learning model to predict the sentiment of  

    Reddit comments.
    """
    def __init__(self):
        self._model, self._vectorizer, self._pca = load_artifacts_from_s3()


    def predict_sentiment(self, df_comments: DataFrame):
        """Preprocess comments and predict sentiment for each of them.

        Parameters
        ----------
        df : Dataframe 
             The comments to be preprocessed and predicted.
        
        Returns
        -------
        df : dataframe with new sentiment column
        """
        applied_vectorization_comments = self._vectorizer.transform(df_comments['body']).toarray()
        applied_pca_comments = self._pca.transform(applied_vectorization_comments)

        #0 = negative, #1 = positive
        prediction_proba = self._model.predict_proba(applied_pca_comments) 
        prediction_score = [reduce(lambda x, y: round(y - x, 4), row) for row in prediction_proba]
    
        df_comments['score'] = prediction_score

        # Drop body column
        df_comments.drop(columns=['body'], inplace=True)
        
        return df_comments