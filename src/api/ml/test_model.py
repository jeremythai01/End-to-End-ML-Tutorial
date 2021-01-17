import model
import pandas as pd

def test_predict_sentiment():   

    ml_model = model.SentimentAnalysisModel()

    df = pd.DataFrame()

    text = ["This is a test sentence", "another one"]

    df['cleaned text'] = text
    
    result_df = ml_model.predict_sentiment(df)

    assert [str(sentiment)[::-1].find('.') > 2 for text, score in result_df.items()]