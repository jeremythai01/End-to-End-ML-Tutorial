import unittest
import re
from src.services.data_prep.text_preprocessor import TextPreprocessor

class TestTextPreprocessor(unittest.TestCase):

    def setUp(self):
        self.textCleaner = TextPreprocessor()


    def test_preprocess_text_check_numbers(self):    

        text = "This is a test sentence 12345 I am happy"

        result_text = self.textCleaner.preprocess_text(text)

        self.assertTrue(any(char.isdigit() for char in result_text) == False)
        

    def test_preprocess_text_check_special_characters(self):    

        text = "This is a test sentence 12345 I am happy"

        result_text = self.textCleaner.preprocess_text(text)

        regex = re.compile('[@_!#$%^&*()<>?/}{~:]') 

        self.assertTrue(regex.search(result_text) == None)