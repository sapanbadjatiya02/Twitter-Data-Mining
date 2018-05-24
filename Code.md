#Predection for facebook stock price:
from stocker import Stocker
import flask
import pygments
from flask_restful import Resource, Api

fbstock = Stocker('FB')
fbstock.plot_stock()
fbstock.evaluate_prediction()
fbbar= fbstock.predict_future(days=100)

# predict days into the future
model, model_data = fbstock.create_prophet_model(days=90)
fbstock.evaluate_prediction(start_date = '2018-04-21', end_date = '2018-04-25', nshares=100)
fbstock.predict_future(days=30)

#Plotting stock price of facebook from 15th March 2018 to 19th April 2018
import csv
import pandas as pd

facebook= pd.read_csv('facebook.csv')
print(facebook.head(5))

from datetime import datetime
facebook['Date'] = pd.to_datetime(facebook['Date'])

print(facebook.dtypes)
facebook.plot(x='Date', y='Low')

import matplotlib.pyplot as plt
from pandas import Series, DataFrame, Panel
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly
print(plotly.__version__)           # version 1.9.4 required
plotly.offline.init_notebook_mode() # run at the start of every notebook
plotly.offline.iplot({
"data": [{
    "x": facebook['Date'],
    "y": facebook['Low']
}],
"layout": {
    "title": "Stock Price", "xaxis": dict(title='DATE'), "yaxis": dict(title='PRICE $')
}
})


#Twitter data analysis
import tweepy
import twitter
import json
import sys
from twitter_login_fn import oauth_login
from twitter_search_fn import twitterSearch
from datetime import datetime
from DB_fn import save_to_DB
import pymongo
import pandas as pd
import numpy as np
import csv

#Makinf mongodb connection
client = pymongo.MongoClient()
client.database_names()

#Creating database deletefacebook
db1 = client.deletefacebook
db1.collection_names()

#Creating collection fb1 in deletefacebook database for tweets ranging from 10th April to 18th April 2018
coll1 = db1.fb1
docs= coll1.find()

fblist = [doc for doc in docs]
print(len(fblist))
print(fblist[0])
print(fblist[-500])

#Creating second collection fb2 for the tweets of 10th and 11th April 2018
coll2 = db1.fb2
docs2= coll2.find()
fblist2 = [doc for doc in docs2]
print(len(fblist2))
print(fblist2[0])
print(fblist2[-1])

#Making a dataframe
fbweekdata = pd.DataFrame()
fbweekdata['id'] = [tweet['id'] for tweet in fblist]
fbweekdata['text'] = [tweet['text'] for tweet in fblist]
fbweekdata['created_at'] = [tweet['created_at'] for tweet in fblist]
fbweekdata['retweeted?'] = [tweet['retweeted'] for tweet in fblist]
fbweekdata['retweet_count'] = [tweet['retweet_count'] for tweet in fblist]
fbweekdata['favorite_count'] = [tweet['favorite_count'] for tweet in fblist]
fbweekdata['lang'] = [tweet['lang'] for tweet in fblist]
fbweekdata['username'] = [tweet['user']['name'] for tweet in fblist]
fbweekdata['usertimezone'] = [tweet['user']['time_zone'] for tweet in fblist]

#getting the list of countries from where tweets were posted
countrylist = []
count = 0
for tweet in fblist:
    if tweet['place'] != None:
        countrylist.append( tweet['place']['country'])
    else:
        countrylist.append(None)
        count += 1

#adding country to fbweekdata
fbweekdata['country'] = countrylist
print(count)

#getting the list of hashtags and saving it in Fbweekdata
hashtaglist= []
for tweet in fblist:
    htags = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
    hashtaglist.append(htags)
fbweekdata['hashtags'] = hashtaglist


#getting a list of mentions and saivng it in Fbweekdata
mentionlist= []
for tweet in fblist:
    mentiontags = [user_mention['screen_name'] for user_mention in tweet['entities']['user_mentions']]
    mentionlist.append(mentiontags)
fbweekdata['User_mentions'] = mentionlist


from datetime import datetime
datelist = []
from datetime import datetime
for tweet in fblist:
    datestr = tweet['created_at']
    # convert the key string to a datetime object
    dt = datetime.strptime(datestr, "%a %b %d %H:%M:%S +0000 %Y")
    datelist.append(dt)

fbweekdata['datetime'] = datelist
fbweekdata['yearmonthday'] = ['%d/%d/%d' % (dt.year,dt.month,dt.day) for dt in fbweekdata['datetime']]

#Checking the dataframe
print(fbweekdata.shape)
print(fbweekdata.head())
outfile = 'fbweekdata.csv'
fbweekdata.to_csv(outfile, header = True)

#Function for getting hashtags and mentions:
def get_entities(tweet):
    if 'entities' in tweet.keys():
        mentions = [user_mention['screen_name'] for user_mention in tweet['entities']['user_mentions']]

        hashtags = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]


        return mentions, hashtags
    else:
        # if no entities key, return empty lists
        return [], []

#List of top 20 frequently mentioned users:
mention_fd = {}
from operator import itemgetter
for tweet in fblist:
        # get the three entity lists from this tweet
    (mentions, hashtags) = get_entities(tweet)
        # put the mentions in the frequency dictionary
    for tag in mentions:
            # if the tag is not yet in the dictionary, add it with the count of 1
        if not tag in mention_fd:
                mention_fd[tag] = 1
        else:
                # otherwise, add 1 to the count that is already there
                mention_fd[tag] += 1

    # sort the dictionary by frequency values, returns a list of pairs of words and frequencies
    #   in decreasing order
mentions_sorted = sorted(mention_fd.items(), key=itemgetter(1), reverse=True)

    # print out the top number of words with frequencies
    # go through the first 20 tweets and find the entities
print("Top", 20, "Frequency Mentions")
for (word, frequency) in mentions_sorted[:20]:
    print (word, frequency)

#List of top 20 frequently used Hashtags:
hashtags_fd = {}
for tweet in fblist:
        # get the three entity lists from this tweet
    (mentions, hashtags) = get_entities(tweet)
        # put the hashtags in the frequency dictionary
    hashlist = []
    for tag in hashtags:
        tag =tag.lower()
        hashlist.append(tag)
    for tag in hashlist:
            # if the tag is not yet in the dictionary, add it with the count of 1
        if not tag in hashtags_fd:
                hashtags_fd[tag] = 1
        else:
                # otherwise, add 1 to the count that is already there
                hashtags_fd[tag] += 1

    # sort the dictionary by frequency values, returns a list of pairs of words and frequencies
    #   in decreasing order
hashtags_sorted = sorted(hashtags_fd.items(), key=itemgetter(1), reverse=True)

    # print out the top number of words with frequencies
    # go through the first 20 tweets and find the entities
print("Top", 20, "Frequency Hashtags")
for (word, frequency) in hashtags_sorted[:20]:

    print (word, frequency)

#sorting the data according to the number of likes and retweets
fbweekdata1 = fbweekdata
Likelihood = (fbweekdata1.sort_values(by =['favorite_count'], ascending  = False))
Retweeting = (fbweekdata1.sort_values(by =['retweet_count'], ascending  = False))
Top20_tweets_by_likes = (Likelihood[['text', 'favorite_count', 'retweet_count']][:20])
Top20_tweets_by_retweets = (Retweeting[['text','retweet_count', 'favorite_count']][:20])

print(Top20_tweets_by_likes)
print(Top20_tweets_by_retweets)

#Printing the language in which tweets have been posted
tweets_by_lang = fbweekdata['lang'].value_counts()
print(tweets_by_lang)

#Retrieving timezones of user profiles
timezone = fbweekdata['usertimezone'].value_counts()
print(timezone)

#getting the list of timezone
timezonelist = []
count = 0
for tweet in fblist:
    if tweet['user']['time_zone'] != None:
        timezonelist.append( tweet['user']['time_zone'])
    else:
        timezonelist.append(None)
        count += 1

#Count of users who have not mentioned their timezones
print(count)

#Creating another dataframe to analyze data of 2 days
fb2daydata = pd.DataFrame()

fb2daydata['id'] = [tweet['id'] for tweet in fblist2]
fb2daydata['text'] = [tweet['text'] for tweet in fblist2]
fallondata['retweeted?'] = [tweet['retweeted'] for tweet in fallonlist]
fb2daydata['lang'] = [tweet['lang'] for tweet in fblist2]
fb2daydata['created_at'] = [tweet['created_at'] for tweet in fblist2]
fb2daydata['retweet_count'] = [tweet['retweet_count'] for tweet in fblist2]
fb2daydata['favorite_count'] = [tweet['favorite_count'] for tweet in fblist2]
fb2daydata['username'] = [tweet['user']['name'] for tweet in fblist2]
fb2daydata['SA'] = np.array([ analize_sentiment(tweet) for tweet in fb2daydata['text'] ])

print(fb2daydata.head())

from textblob import TextBlob
import re

def clean_tweet(tweet):
    '''
    Utility function to clean the text in a tweet by removing
    links and special characters using regex.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analize_sentiment(tweet):
    '''
    Utility function to classify the polarity of a tweet
    using textblob.
    '''
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1

# We create a column with the result of the analysis:
fbweekdata['SA'] = np.array([ analize_sentiment(tweet) for tweet in fbweekdata['text'] ])

# We display the updated dataframe with the new column:
print(fbweekdata.head(10))

#Sentiment Analysis:
# We construct lists with classified tweets:

pos_tweets = [ tweet for index, tweet in enumerate(fb2daydata['text']) if fb2daydata['SA'][index] > 0]
neu_tweets = [ tweet for index, tweet in enumerate(fb2daydata['text']) if fb2daydata['SA'][index] == 0]
neg_tweets = [ tweet for index, tweet in enumerate(fb2daydata['text']) if fb2daydata['SA'][index] < 0]


print("Percentage of positive tweets: {}%".format(len(pos_tweets)*100/len(fb2daydata['text'])))
print("Percentage of neutral tweets: {}%".format(len(neu_tweets)*100/len(fb2daydata['text'])))
print("Percentage de negative tweets: {}%".format(len(neg_tweets)*100/len(fb2daydata['text'])))
