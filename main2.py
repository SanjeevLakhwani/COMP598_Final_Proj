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

df = pd.DataFrame()


def authorize():
    api = tp.Client(bearer_token=os.environ.get("bearer_token"))
    print("Authenticated")
    return api


def init_df():
    global df
    data = {"id": [], "text": [], "topic": [], "emotion": []}
    df = pd.DataFrame(data)
    df = df.astype({"id": int, "text": str, "topic": str, "emotion": str})


def add_data(data):
    global df
    for tweet in data:
        df = df.append({"id": tweet.id,
                        "text": tweet.text,
                        "topic": "",
                        "emotion": ""}, ignore_index=True)
    df = df.drop_duplicates(subset=["id"])
    return df.shape[0]


def collect_data(api, min_tweet_count):
    print("Collecting data...")
    query = "((covid or #covid) OR (vaccination OR #vaccination OR vaccine OR #vaccine) OR pfizer OR moderna or " \
            "astrazeneca) -is:retweet lang:en "
    max_tweets = 100
    next_token = None
    start_time = datetime.fromisoformat("2021-12-03")
    end_time = start_time + timedelta(3)
    t_count = 0
    init_df()
    
    while t_count < min_tweet_count:
        res = api.search_recent_tweets(query=query, 
                                       max_results=max_tweets,
                                       start_time=start_time, 
                                       end_time=end_time, 
                                       next_token=next_token)
        t_count = add_data(res.data)
        next_token = res.meta["next_token"]
        print(f"Collected {t_count} tweets")
    print("Data Collected")


def save_data(file_name):
    global df
    print("Saving Data")
    df.to_csv(file_name)
    print("Data Saved")

def main():
    api = authorize()
    collect_data(api, 1200)
    save_data("tweets5.csv")


if __name__ == '__main__':
    main()
