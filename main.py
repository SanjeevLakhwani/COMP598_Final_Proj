import datetime

import tweepy as tp


def main():
    cl = tp.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAALNTWAEAAAAA99a%2B42EREAAKFnNFsaIc0mfb65c%3D824aYlAkcr50Yr3CsOiGbwO55VJg2KcRB9E0QdHAM4FQ8drMOV")

    options = {
        "query": "covid",
        "end_time": "2021-06-23T09:07:21-07:00",  # YYYY-MM-DDTHH:mm:ssZ
        "max_results": 2,
        # "next_token": "",
        "start_time": "2021-07-23T09:07:21-07:00"
    }

    res = cl.search_all_tweets(query="covid")
    print(res)


if __name__ == '__main__':
    main()