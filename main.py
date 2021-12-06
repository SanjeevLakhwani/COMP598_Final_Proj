import pprint
import pandas as pd
import argparse
import tweepy
import tweepy as tp
import os
from dotenv import load_dotenv

load_dotenv()


def authorize_v2():
    api = tp.Client(bearer_token=os.environ.get("bearer_token"),
                    consumer_key=os.environ.get("consumer_key"), consumer_secret=os.environ.get("consumer_secret"),
                    access_token=os.environ.get("access_token"),
                    access_token_secret=os.environ.get("access_token_secret"))
    return api


def get_tweets_v2(api):
    query = "((covid or #covid) OR (vaccination OR #vaccination OR vaccine OR #vaccine) OR pfizer OR moderna or " \
            "astrazeneca) -is:retweet lang:en "
    date1 = "2021-07-09T12:22:09.1440844-07:00"
    date2 = "2021-01-09T12:22:09.1440844-07:00"
    f = api.search_recent_tweets(query=query,max_results=10, end_time=date1,start_time=date2)
    # start time can be up to 7 days ago
    # end time should be 3 days after start time
    # max_results up to 100, call it 10 times?
    # f = api.search_recent_tweets(query=query, max_results=10)
    for tweet in f[0]:
        print(tweet)
        print("========================================================================================")


def main():
    api = authorize_v2()
    get_tweets_v2(api)


if __name__ == '__main__':
    main()