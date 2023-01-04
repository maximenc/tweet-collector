import pandas as pd
import tweepy
from time import sleep
import json
import html

# Read token and secret from the json file
with open('api-key-secret.json', 'r') as f:
    config = json.load(f)

# Authenticate the API connection
client = tweepy.Client(
                bearer_token=config["bearer_token"],
                consumer_key=config["consumer_key"],
                consumer_secret=config["consumer_secret"],
                access_token=config["access_token"],
                access_token_secret=config["access_token_secret"],
                wait_on_rate_limit=True)

def get_tweets(query, start_datetime, end_datetime):
    """
    Retrieve tweets using the API and return a dataframe that contains the tweets.
    
    Parameters:
        query (str): The search query.
        start_datetime (str): The oldest UTC timestamp from which the Tweets will be provided.
        end_datetime (str): The newest, most recent UTC timestamp to which the Tweets will be provided.
    
    Returns:
        A dataframe that contains the tweets.
    """
    
    # Initialize variables and dictionaries
    count_response = None
    next_token = None
    result = []
    user_dict = {}
    place_dict = {}

    while True:
        try:
            response = client.search_all_tweets(
                query,
                next_token = next_token,
                # define the maximum number of tweets to retrieve
                max_results = 500,
                # The newest, most recent UTC timestamp to which the Tweets will be provided.
                end_time = end_datetime,
                # The oldest UTC timestamp from which the Tweets will be provided.
                start_time = start_datetime,
                place_fields = ['country', 'country_code'],
                user_fields = ['username', 'public_metrics', 'description',
                              'location', 'created_at', 'entities', 'url', 'verified'],
                tweet_fields = ['id', 'created_at', 'geo', 'entities', 'lang',
                               'public_metrics', 'source'],
                expansions = ['author_id', 'geo.place_id', 'in_reply_to_user_id'],  
            )
        except (tweepy.errors.TwitterServerError) as e:
            # if there is a connexion error, sleep for 10 seconds and continue
            print(e)
            print("sleep 10secs")
            sleep(10)
            continue

        count_response = response.meta["result_count"]

        print("", count_response)
        # if the api returns empty response then end the collect
        if count_response == 0:
            break
        
        # compile all the information about the users into a dictionay: user_dict
        for user in response.includes['users']:
            user_dict[user.id] = {'name':user.name,
                                'username': user.username,
                                'created_at': user.created_at,
                                'description': user.description, 
                                'entities': user.entities, 
                                'location': user.location, 
                                'pinned_tweet_id':user.pinned_tweet_id,
                                'protected':user.protected,
                                'followers_count': user.public_metrics['followers_count'], 
                                'following_count': user.public_metrics['following_count'], 
                                'tweet_count': user.public_metrics['tweet_count'],
                                'listed_count': user.public_metrics['listed_count'],
                                'url':user.url, 
                                'verified':user.verified 
                                }

        # Compile all the information about the location into a dictionary: place_dict
        for place in response.includes['places']:
            place_dict[place.id] = {'geo_id':place.id,
                                    'full_name':place.full_name,
                                    'country': place.country, 
                                    'place_type': place.place_type
                                    }
        # loop through all the tweets to add the information from the user (user_dict)
        # and from the location (place_dict)
        for tweet in response.data:
            # For each tweet, we find the author's informations and location informations
            # and we put all of the information we want to keep in a single dictionary for each tweet
            author_info = user_dict[tweet.author_id]
            geo_info =  place_dict[place.id]

            # we format the text of the tweet
            raw_text = str(html.unescape(tweet.text))
            raw_text = raw_text.encode('ascii',errors='ignore')
            raw_text = raw_text.decode('ascii')
            raw_text = raw_text.lower()

            # create a variable that will contains a list of hashtags mentioned in the tweet
            try:
                hashtags = [tg["tag"].upper() for tg in tweet.entities['hashtags']]
            except (KeyError, TypeError):
                hashtags = []
            
            # same for cashtags
            try:
                cashtags = [tg["tag"].upper() for tg in tweet.entities['cashtags']]
            except (KeyError, TypeError):
                cashtags = []

            # same for mentions
            try:
                mentions = [tg["username"].upper() for tg in tweet.entities['mentions']]
            except (KeyError, TypeError):
                mentions = []

            # create a dictionary that will be line in the dataframe
            line = {
                '_id': tweet.id,
                'created_at': tweet.created_at, 
                'author_id': tweet.author_id,                            
                'author_verified': author_info['verified'],
                'text': raw_text,
                'lang': tweet.lang,
                'retweet_count': tweet.public_metrics['retweet_count'], 
                'reply_count': tweet.public_metrics['reply_count'],
                'like_count': tweet.public_metrics['like_count'],
                'quote_count': tweet.public_metrics['quote_count'],
                'cashtags': cashtags,
                'hashtags': hashtags,
                'mentions': mentions
                }
            """
                other informations that can be added in the dataframe:
                'username': author_info['username'],
                'author_created_at': author_info['created_at'],
                'author_description': author_info['description'],
                'author_entities': author_info['entities'],
                'author_location': author_info['location'],
                'pinned_tweet_id': author_info['pinned_tweet_id'],
                'protected': author_info['protected'],
                'author_followers': author_info['followers_count'],
                'author_following': author_info['following_count'],
                'author_tweet_count': author_info['tweet_count'],                       
                'author_listed_count': author_info['listed_count'],
                'author_url': author_info['url'],
                'geo': tweet.geo, 
                'entities': tweet.entities,
                'non_public_metrics': tweet.non_public_metrics, 
                'in_reply_to_user_id': tweet.in_reply_to_user_id, 
                'source': tweet.source, 
                'geo_id': geo_info['geo_id'],
                'full_name': geo_info['full_name'], 
                'country': geo_info['country'],
                'place_type': geo_info['place_type']
            """

            result.append(line)
        try:
            next_token = response.meta["next_token"]
        except KeyError:
            break
    
    print("total number of tweets: ", len(result))
    df = pd.DataFrame.from_dict(result)
    return df