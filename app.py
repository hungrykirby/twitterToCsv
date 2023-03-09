import os
from os.path import join, dirname
from dotenv import load_dotenv

import Tweet
import CsvGenerate

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

data_path = os.environ.get('TWITTER_DATA_PATH')
user_id = os.environ.get('TWITTER_USER_ID')

if __name__ == '__main__':
    t = Tweet.Tweet(data_path, user_id)
    tweets_list = t.call_with_pictures()

    csv_gemerator = CsvGenerate.CsvGenerator()
    csv_gemerator.set_export_list(tweets_list)
    csv_gemerator.call()
