import pandas as pd
import argparse
import tweepy as tp
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("-o", default="tweets2.csv", type=str)
parser.add_argument("--verbose", default=True, type=bool)
parser.add_argument("--tweet_count", default=1200, type=int)
parser.add_argument("--step_size", default=100, type=int)
args = parser.parse_args()

df = pd.DataFrame()

if args.verbose:
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
else:
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.CRITICAL)


def authorize():
    api = tp.Client(bearer_token=os.environ.get("bearer_token"))
    logging.info("Authenticated")
    return api


def init_df():
    global df
    data = {"id": [], "text": [], "topic": [], "emotion": []}
    df = pd.DataFrame(data)
    df = df.astype({"id": str, "text": str, "topic": str, "emotion": str})


def add_data(data):
    global df
    for tweet in data:
        df = df.append({"id": tweet.id,
                        "text": tweet.text,
                        "topic": "",
                        "emotion": ""}, ignore_index=True)
    df = df.drop_duplicates(subset=["id"])
    return df.shape[0]


def collect_data(api, min_tweet_count, step_size):
    logging.info("Collecting data...")
    query = "(((covid OR #covid) (vaccination OR #vaccination OR vaccine OR #vaccine)) OR pfizer OR moderna or " \
            "astrazeneca) -is:retweet lang:en"
    max_tweets = step_size
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
        logging.info(f"Collected {t_count} tweets")
    logging.info("Data Collected")


def save_data(file_name):
    global df
    logging.info("Saving Data")
    df.to_csv(file_name, index=False)
    logging.info("Data Saved")


def main():
    output_file = args.o
    min_tweet_count = args.tweet_count
    step_size = args.step_size
    api = authorize()
    collect_data(api, min_tweet_count, step_size)
    save_data(args.o)


if __name__ == '__main__':
    main()
