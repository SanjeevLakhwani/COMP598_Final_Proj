import pprint
import pandas as pd
import argparse
import tweepy
import tweepy as tp
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("-o", default="output.csv")
args = parser.parse_args()
verbose = True

def authorize():
    # api = tp.Client(bearer_token=os.environ.get("bearer_token"),
    #                 consumer_key=os.environ.get("consumer_key"), consumer_secret=os.environ.get("consumer_secret"),
    #                 access_token=os.environ.get("access_token"),
    #                 access_token_secret=os.environ.get("access_token_secret"))
    api = tp.Client(bearer_token=os.environ.get("bearer_token"))
    print("Authenticated")
    return api


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
    query = "((covid or #covid) OR (vaccination OR #vaccination OR vaccine OR #vaccine) OR pfizer OR moderna or " \
            "astrazeneca) -is:retweet lang:en "
    max_results = 11
    print("Request Sent")
    res = api.search_recent_tweets(query=query, max_results=max_results)
    print("Data Recieved")
    if verbose:
        print("===========RESPONSE===============")
        print("=======META=========")
        print(res.meta)
        print("=======DATA=========")
        for tweet in res.data:
            print("----")
            print(tweet.id)
            print(tweet.text)
            print("----")
        print("==================================")
    return res


def init_df():
    data = {"id": [], "text": [], "topic": [], "emotion": []}
    return  pd.DataFrame(data)


def add_data(df, data):
    for tweet in data:
        df = df.append({"id": tweet.id,
                        "text": tweet.text,
                        "topic": "",
                        "emotion": ""}, ignore_index=True)
    df.drop_duplicates(subset=["id"])
    return df




def collect_data(api, min_tweet_count):
    query = "((covid or #covid) OR (vaccination OR #vaccination OR vaccine OR #vaccine) OR pfizer OR moderna or " \
            "astrazeneca) -is:retweet lang:en "
    max_tweets = 100
    next_token = None
    start_time = datetime.fromisoformat("20121-12-03")
    end_time = start_time + timedelta(3)
    t_count = 0
    df = init_df()
    
    while t_count < min_tweet_count:
        res = api.search_recent_tweets(query=query, 
                                       max_tweets=max_tweets, 
                                       start_time=start_time, 
                                       end_time=end_time, 
                                       next_token=next_token)
        t_count = add_data(df, res.data)
        next_token = res.meta["next_token"]


def main():
    api = authorize()
    tweets = get_tweets(api)
    # store_tweets(tweets, args.o)


if __name__ == '__main__':
    main()
