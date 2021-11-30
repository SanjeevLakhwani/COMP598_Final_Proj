import pandas as pd
import pprint
import tweepy
import tweepy as tp


def authorize():
def add(df, data):

def main():
    auth = tp.OAuthHandler(consumer_key="qgVsLBKbmjFxDoodyWVX1k3dx", consumer_secret="8z3y934Na5IgfO4u791kDrzQ45EPDSmJfCGB6AvYIwoqM2Pu3w")
    auth.set_access_token("1462918284601225216-E7VWlZvm2AJXOJAmg5HP94WdfNSjB4", "tvs1Phv1Bg4bKugrhDclZprbLvpaJBDHIo37NVBIl8hLc")

    api = tweepy.API(auth)

    # api.search_tweets()

    f = api.search_tweets(q="covid", count=1)
    print(len(f))

    # print(pprint.pprint(f[0]._json))


if __name__ == '__main__':
    main()