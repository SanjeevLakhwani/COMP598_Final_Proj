import tweepy as tp


def main():
    cl = tp.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAARUWAEAAAAA1pIyAuyOpmUQmDvugNdXuf0nYYI%3DnvCTS784Hq2ZFq06wZz8QprQA4B2fGhX7BdkhBgOpx0yYy5f4o")

    a = cl.search_recent_tweets(query="covid")
    print(a)


if __name__ == '__main__':
    main()