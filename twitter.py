import json
import tweepy as tw

# Change these personal keys
CONSUMER_KEY = '46ue77KJ3l3ut1ITSPBb51csI'
CONSUMER_SECRET = 'W4bbATMnaCRNe0QQqEhq98wTjgtRh6BdlkJRbdcz3IUSWQdjkK'
ACCESS_TOKEN = '1385510822630330371-OcSJa7Ga1wpoG8NxGrDnBpBheaSM8A'
ACCESS_TOKEN_SECRET = 'kOm9mTCIRWbt1Sft6rZNl3tfKlcyB8HjYF0DX7nQHImsC'

# Instantiate a client
auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)

# Twitter API only allows you to access the past few weeks of tweets.
search_words = "#visittrentino"

tweets = tw.Cursor(api.search_tweets,
                   q=search_words,
                   #geocode="46.06787,11.1210,50km",  # geocode for trento +radius of 50 km
                   tweet_mode='extended',
                   lang="en").items(500)  # european languages

output_list = []
for tweet in tweets:
    output_list.append(json.load(tweet._json))

all_items = []
for json_file in output_list:
    all_items += json_file['items']

with open('twitter_data.json', 'w') as f:
    json.dump({"items": all_items}, f, textfile_merged)


