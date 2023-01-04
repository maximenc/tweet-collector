import pandas as pd
import datetime
from time import sleep
from os import listdir
from os.path import isfile, join
import fetch_api

"""
The code iterates through the list of companies and their cashtags in the csv file "sp100.csv",
constructs a search query using the company name and cashtag,
sets the start and end dates for the tweet search,
and retrieves the tweets using the get_tweets function.

"""

# The parameters of the query:
year = 2018
#month = 1
path = "data/%s/" % str(year)
end_datetime = datetime.datetime(year+1, 1, 1, 0, 0, 0)
start_datetime = datetime.datetime(year, 1, 1, 0, 0, 0)
output_file = "data/" + str(year) + "/%s" + "_" + str(year) + ".csv"
#output_file = "data/" + str(year) + "/%s" + str(month) + "/" + ticker + "_" + str(year) + "_" + str(month) + ".csv"

# create a list of ticker to ignore from the S&P 100 list
list_ticker_ignored = ["AAPL", "NFLX"]

# 
df_comp = pd.read_csv("data/sp100.csv")
df_comp["mention"] = df_comp["mention"].astype(str)
df_comp["mention"] = df_comp["mention"].replace(",", " OR", regex=True)
df_comp["name"] = df_comp["name"].astype(str)
df_comp["name"] = df_comp["name"].replace(", ", "\" OR \"", regex=True)
df_comp = df_comp.replace("nan", "")
list_ticker = list(df_comp["ticker"].values)

# Create a list of tickers that are already in the folder
list_files = [f for f in listdir(path) if isfile(join(path, f))]
ticker_file = [file.split("_")[0] for file in list_files]
print("The following firms have already been collected for %s: %s" % (year, ticker_file))

# Remove the tickers already collected from the list 
for tck in ticker_file:
    list_ticker.remove(tck)

# Remove the tickers to ignore
for tck in list_ticker_ignored:
    try:
        list_ticker.remove(tck)
    except ValueError:
        pass

def get_df(ticker, name=False):
    """
    This function is used to build the query based on the company twitter.
    It then call get_tweets to create a dataframe of the tweets.

    if name=True then the company name is used in the query to collect the tweets.
    """

    # Test mention query
    mention = list(df_comp.loc[df_comp.ticker==ticker,"mention"])[0]
    if mention == "":
        mention = ""
    else:
        mention = " OR " + mention

    # Test name query
    name = list(df_comp.loc[df_comp.ticker==ticker,"name"])[0]
    if name == "":
        name = ""
    else:
        name = " OR \"" + name + "\""

    # include the company name in the query if name == True
    if name == True:
        query = "$" + ticker + mention + name +  " lang:en -is:retweet"
    else:
        query = "$" + ticker + mention +  " lang:en -is:retweet"
    print("query: ", query)
    
    df = fetch_api.get_tweets(query, start_datetime, end_datetime)
    output_file_name = output_file % ticker

    try:
        df.to_csv(output_file_name)
    except:
        print("error while saving to csv for ticker: ", ticker)
        sleep(10)

for tck in list_ticker:
    mention = list(df_comp.loc[df_comp.ticker==tck,"mention"])[0]
    get_df(tck, mention)
