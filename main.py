import datetime

import tweepy as tp
import csv
con_key = "qgVsLBKbmjFxDoodyWVX1k3dx"
con_secret = "8z3y934Na5IgfO4u791kDrzQ45EPDSmJfCGB6AvYIwoqM2Pu3w"
access_key = "1462918284601225216-E7VWlZvm2AJXOJAmg5HP94WdfNSjB4"
access_secret = "tvs1Phv1Bg4bKugrhDclZprbLvpaJBDHIo37NVBIl8hLc"

def get_tweets(api):
    search_words = ["covid", 'vaccine']
    
    tweets = tp.Cursor(api.search_tweets,
                    q=search_words,
                    lang="en",
                    tweet_mode='extended').items(10)
    tweet_text = []
    for tweet in tweets:
        # print(dir(tweet))
        if 'retweeted_status' in dir(tweet):
            tweet_text.append([tweet.retweeted_status.full_text,tweet.created_at])
        else:
            tweet_text.append([tweet.full_text,tweet.created_at])
    #tweet_text = [tweet.full_text for tweet in tweets]
    with open("tweets.csv", 'w', encoding='utf8') as fp:
        tweet_writer = csv.writer(fp)
        tweet_writer.writerow(["Tweet Text","Date"])
        for line in tweet_text:
            tweet_writer.writerow(line)



def main():
    auth = tp.OAuthHandler(con_key,con_secret)
    auth.set_access_token(access_key,access_secret)
    api = tp.API(auth, wait_on_rate_limit=True)
    cl = tp.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAARUWAEAAAAA1pIyAuyOpmUQmDvugNdXuf0nYYI%3DnvCTS784Hq2ZFq06wZz8QprQA4B2fGhX7BdkhBgOpx0yYy5f4o")
    # a = cl.search_recent_tweets(query="covid")
    get_tweets(api)


if __name__ == '__main__':
    main()