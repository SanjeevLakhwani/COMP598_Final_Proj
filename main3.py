from logging import raiseExceptions
import pprint
import pandas as pd
import argparse
import tweepy
import tweepy as tp
import csv

from dotenv import load_dotenv

load_dotenv()

import os

parser = argparse.ArgumentParser()
parser.add_argument("-o", default="output.csv")
args = parser.parse_args()


def authorize_v2():
    api = tp.Client(bearer_token=os.environ.get("bearer_token"),
    consumer_key=os.environ.get("consumer_key"), consumer_secret=os.environ.get("consumer_secret"),
    access_token=os.environ.get("access_token"),access_token_secret=os.environ.get("access_token_secret"))
    return api


def get_tweets_v2(api):
    query = "((covid or #covid) OR (vaccination OR #vaccination OR vaccine OR #vaccine) OR pfizer OR moderna or astrazeneca) -is:retweet lang:en "
    obtained = []
    until_id = None
    next_token = None
    
    while (len(obtained) <= 1200):
        f = api.search_recent_tweets(query=query,max_results=100,until_id=until_id,next_token=next_token)
        print(f[3])
        for tweet in f[0]:
            obtained.append(tweet)
        try:
            until_id = f[3]['newest_id']
            next_token = f[3]['next_token']
        except:
            until_id = f[3]['newest_id']
            next_token = None
    return obtained


def get_tweets(api):
    f = api.search_tweets(q="covid", count=1)
    pprint.pprint(f[0]._json)
    return f


def main():
    api = authorize_v2()
    tweets = get_tweets_v2(api)
    with open('tweets.csv', 'w',encoding='utf8') as fp:
        tweetWriter = csv.writer(fp)
        tweetWriter.writerow(["Text", 'Annotations'])
        for tweet in tweets:
            tweetWriter.writerow([str(tweet)])

    # store_tweets(tweets, args.o)


if __name__ == '__main__':
    main()
