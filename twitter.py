import json
import tweepy as tw

class twitterAPI:

    def __init__(self, search_word="#visittrentino"):
        self.CONSUMER_KEY = '46ue77KJ3l3ut1ITSPBb51csI'
        self.CONSUMER_SECRET = 'W4bbATMnaCRNe0QQqEhq98wTjgtRh6BdlkJRbdcz3IUSWQdjkK'
        self.ACCESS_TOKEN = '1385510822630330371-OcSJa7Ga1wpoG8NxGrDnBpBheaSM8A'
        self.ACCESS_TOKEN_SECRET = 'kOm9mTCIRWbt1Sft6rZNl3tfKlcyB8HjYF0DX7nQHImsC'
        self.search_word = search_word

    def search_tweets(self, n_tweets=500):
        """
        The function instantiates a client and downloads n tweets
        containing the hashtag specified within the api.
        """
        # Instantiate a client
        auth = tw.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
        api = tw.API(auth, wait_on_rate_limit=True)

        # download info about 500 tweets
        tweets = tw.Cursor(api.search_tweets,
                           q=self.search_word,
                           # geocode="46.06787,11.1210,50km",  # geocode for trento +radius of 50 km
                           tweet_mode='extended',
                           lang="en").items(n_tweets)  # european languages
        return tweets

    def parsing_tweets(self):
        """
        Parsing only the interesting parts within the tweets.
        :return:
        """
        tweets = self.search_tweets()
        # save the tweets in a json file
        output = []

        including_lst = ["created_at", "full_text", "entities", "metadata", "source",
                         "geo","coordinates", "place", "contributors", "is_quote_status",
                         "retweet_count", "favorite_count", "favorited", "retweeted", "lang"]

        for tweet in tweets:
            new_data = dict()
            for item in tweet._json:
                if item in including_lst:
                    new_data[item] = tweet._json[item]
            output.append(new_data)

        with open('twitter_data.json', 'w') as f:
            json.dump(output, f, indent=2)




