#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import re
import regex
from services.api.ml import text_cleaner


def test_preprocess_text_check_numbers():    

    text = [{"text" : "This is a test sentence 12345 I am happy"}]

    df = pd.DataFrame(text)

    preprocessor = text_cleaner.Preprocessing()

    result_df = preprocessor.preprocess_text(df)

    cleaned_text = result_df['cleaned text'][0]

    assert any(char.isdigit() for char in cleaned_text) == False
    

def test_preprocess_text_check_special_characters():    

    text = [{"text" : "This is a , test sentence, I am happy!!."}]

    df = pd.DataFrame(text)

    preprocessor = text_cleaner.Preprocessing()

    result_df = preprocessor.preprocess_text(df)

    cleaned_text = result_df['cleaned text'][0]

    regex = re.compile('[@_!#$%^&*()<>?/}{~:]') 

    assert regex.search(cleaned_text) == None