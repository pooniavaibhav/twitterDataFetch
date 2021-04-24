
# import modules
import pandas as pd
import tweepy
_hashtags = ""
_mention = ""


def scrape(words, date_since, numtweet,api):
    # Creating DataFrame using pandas
    db = pd.DataFrame(columns=['username', 'date', 'retweets',
                               'favorites','text', 'geo', 'mentions', 'hashtags', 'id','permalink'])

    tweets = tweepy.Cursor(api.search, q=words, lang="en",
                           since=date_since, tweet_mode='extended').items(numtweet)

    list_tweets = [tweet for tweet in tweets]
    i = 1
    for tweet in list_tweets:
        username = tweet.user.screen_name
        date = tweet.created_at
        location = tweet.user.location
        retweetcount = tweet.retweet_count
        mentions = clean_mentions(tweet.entities['user_mentions'])
        hashtags = clean_hashtag(tweet.entities['hashtags'])
        user = api.get_user(username)
        user_id = user.id_str
        favorites = user.favourites_count
        permalink = user.profile_image_url
        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text


        # Here we are appending all the extracted information in the DataFrame
        ith_tweet = [username,date,retweetcount,
                     favorites,
                     text,location,mentions,hashtags, user_id,
                     permalink
                     ]
        db.loc[len(db)] = ith_tweet

        i = i + 1
    filename = 'scraped_tweets.csv'

    # we will save our database as a CSV file.
    db.to_csv("data.csv")

def clean_hashtag(tag):
    global _hashtags
    _hashtag = ""
    if tag:
        for key,value in tag[0].items():
            if key == 'text':
                _hashtags = _hashtags + "#" + value
        return(_hashtags)
    else:
        return([])


def clean_mentions(mention):
    global _mention
    _mention = ""
    if mention:
        for key,value in mention[0].items():
            if key == 'screen_name':
                _mention = _mention + value
        return(_mention)
    else:
        return []

if __name__ == '__main__':
    # Enter your own credentials obtained
    consumer_key = ""
    consumer_secret = ""
    access_key = ""
    access_secret = "
"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # Enter Hashtag and initial date
    #print("Enter Twitter HashTag to search for")
    words = input()
   # print("Enter Date since The Tweets are required in yyyy-mm--dd")
    date_since = "2021-04-20"

    # number of tweets you want to extract in one run
    numtweet = 10
    scrape(words, date_since, numtweet,api)
    print('Scraping has completed!')
