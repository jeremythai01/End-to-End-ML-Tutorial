
from typing import Dict
import unittest
from services.data_scrape.reddit_bot import RedditBot

class TestRedditBot(unittest.TestCase):

    def setUp(self):
        self.bot_1 = RedditBot.getInstance()


    def test_getInstance(self):    
        bot_2 = RedditBot.getInstance()
        self.assertEqual(self.bot_1, bot_2)


    def test_scrape_reddit(self):
        data = self.bot_1.scrape_reddit("Stocks", 1)
        LENGTH_DICT = 10
        for c_info in data:
            self.assertIsInstance(c_info, Dict)
            self.assertEqual(len(c_info), LENGTH_DICT)
            for key, value in c_info.items():
                self.assertIsNotNone(value)
                self.assertIsInstance(value, str)