# tweet-collector

This is a Twitter scraper that collects tweets about companies in the S&amp;P 100 index using the Twitter research API. The scraper preprocesses the data and outputs it as a CSV file, making it easy to analyze and visualize trends and patterns in the tweets. The collected data can be used for various purposes, such as sentiment analysis, brand monitoring, and market research.

## Requirement 
- Twitter API v2 access: sign up for a Twitter Developer account (if you don't already have one) and create a new project. Generate a bearer token and API keys for your project. You will need to provide these API keys and the bearer token when authenticating the API connection.
- Install the required libraries: pandas, tweepy
- create a "api-key-secret.json" that will contains the API access token and secret:

``
{"consumer_key": "YOUR_CONSUMER_KEY", 
"consumer_secret": "YOUR_CONSUMER_SECRET",
"access_token": "YOUR_ACCESS_TOKEN",
"access_token_secret": "YOUR_ACCESS_TOKEN_SECRET",
"bearer_token": "YOUR_BEARER_TOKEN"
}
``

## Function Parameters
The get_tweets function in fetch_api.py has three required parameters:

- query: a string representing the search query. You can use hashtags, keywords, and other advanced search operators to refine your search.
- start_datetime: a string representing the oldest UTC timestamp from which the tweets will be provided. This should be in the format YYYY-MM-DDTHH:MM:SSZ.
- end_datetime: a string representing the newest, most recent UTC timestamp to which the tweets will be provided. This should be in the format YYYY-MM-DDTHH:MM:SSZ.

## Usage
Retrieve tweets from the past week that contain the cashtag $AAPL
``
import fetch_api

start_datetime = "2022-01-01T00:00:00Z"
end_datetime = "2022-01-08T00:00:00Z"
query = "$AAPL"
tweets_df = fetch_api.get_tweets(query, start_datetime, end_datetime)
print(tweets_df.head())
``
## Collect tweets for S&amp;P 100 index members

a Python code is given in "collect.py" to collect all tweets that mentioned the companies in the S&P 100 index, along with their respective cashtags, during a specified year.
