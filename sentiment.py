import numpy as np
import pandas as pd
import tweepy
from tweepy import OAuthHandler

# Keys and tokens of Twitter console
consumer_key = 'Sec3MvclRIx2RVlgu9l0SJX6D'
consumer_secret = 'ayoPNWtBm7fWpMBoK6EwRmegu3SW8Rw9mzJkottkv97quPe941'
access_token = '736550752760406018-so5CPJrEbJKb3c3Pq8va3VFr0yk4S0E'
access_token_secret = 'Cgr8tz0h6FTU7kxAjDzpHnjffNTHxWsBytXnu4Ihd1TFb'

# Function for fetching random tweets from Twitter
# Create tweepy API object to fetch tweets
class TwitterClient(object):
    def __init__(self):
        try:
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        except tweepy.TweepError as e:
            print(f"Error: Twitter Authentication Failed - \n{str(e)}")

    def get_tweets(self, query, maxTweets=1000):
        tweets = []
        sinceId = None
        max_id = -1
        tweetCount = 0
        tweetsPerQry = 100

        while tweetCount < maxTweets:
            try:
                if max_id <= 0:
                    if not sinceId:
                        new_tweets = self.api.search(q=query, count=tweetsPerQry)
                    else:
                        new_tweets = self.api.search(q=query, count=tweetsPerQry, since_id=sinceId)
                else:
                    if not sinceId:
                        new_tweets = self.api.search(q=query, count=tweetsPerQry, max_id=str(max_id - 1))
                    else:
                        new_tweets = self.api.search(q=query, count=tweetsPerQry, max_id=str(max_id - 1), since_id=sinceId)

                if not new_tweets:
                    print("No more tweets found")
                    break

                for tweet in new_tweets:
                    parsed_tweet = {'tweets': tweet.text}
                    if tweet.retweet_count > 0:
                        if parsed_tweet not in tweets:
                            tweets.append(parsed_tweet)
                    else:
                        tweets.append(parsed_tweet)

                tweetCount += len(new_tweets)
                print("Downloaded {0} tweets".format(tweetCount))
                max_id = new_tweets[-1].id

            except tweepy.TweepError as e:
                print("Tweepy error: " + str(e))
                break

        return pd.DataFrame(tweets)

# Calling function to get tweets
twitter_client = TwitterClient()
tweets_df = twitter_client.get_tweets('AI and Deep learning', maxTweets=1000)
print(f'tweets_df Shape - {tweets_df.shape}')
tweets_df.head(10)

# MODULE-1: IDENTIFYING SENTIMENTS SAMPLE CODE
from textblob import TextBlob

# Fetch sentiments using TextBlob
def fetch_sentiment_using_textblob(text):
    analysis = TextBlob(text)
    return 'pos' if analysis.sentiment.polarity >= 0 else 'neg'

# Counts the number of positive and negative tweets
sentiments_using_textblob = tweets_df.tweets.apply(lambda tweet: fetch_sentiment_using_textblob(tweet))
print(pd.DataFrame(sentiments_using_textblob.value_counts()))

# Show the polarity of the fetched tweets using TextBlob
tweets_df['sentiment'] = sentiments_using_textblob
tweets_df.head()
