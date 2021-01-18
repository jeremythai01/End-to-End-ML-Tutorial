#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from ml import model


def test_predict_sentiment():   

    ml_model = model.SentimentAnalysisModel()

    df = pd.DataFrame()

    text = ["This is a test sentence", "another one"]

    df['text'] = text
    
    result_df = ml_model.predict_sentiment(df)

    assert [str(sentiment)[::-1].find('.') > 2 for text, sentiment in result_df.items()]