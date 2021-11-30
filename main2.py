import pprint
import pandas as pd
import argparse
import tweepy
import tweepy as tp

from dotenv import load_dotenv

load_dotenv()

import os

parser = argparse.ArgumentParser()
parser.add_argument("-o", default="output.csv")
args = parser.parse_args()


def authorize():
    auth = tp.OAuthHandler(os.environ.get("consumer_key"), os.environ.get("consumer_secret"))
    auth.set_access_token(os.environ.get("access_token"), os.environ.get("access_token_secret"))
    return tweepy.API(auth)


def store_tweets(tweets, output_file):
    data = {"id": [], "url": [], "text": [], "topic": [], "emotion": []}
    df = pd.DataFrame(data)
    for tweet in tweets:
        df = df.append({"id": tweet["id"],
                        "url": tweet["entities"]["urls"]["url"],
                        "text": tweet["text"],
                        "topic": "",
                        "emotion": ""}, ignore_index=True)
    df.to_csv(output_file)


def get_tweets(api):
    f = api.search_tweets(q="covid", count=1)
    pprint.pprint(f[0]._json)
    return f


def main():
    api = authorize()
    tweets = get_tweets(api)
    store_tweets(tweets, args.o)


if __name__ == '__main__':
    main()
