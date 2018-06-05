''' The main topic search function for Twitter using the python twitter package
      Tries to get up to 1000 results from the Twitter REST/Search API search function
        using the Twitter 'nextresults' parameter for repeated querying
        going back in time from current moment
      Allows keyword parameters
    Utility function to get earliest tweet id from a collection of tweets
    Usage:
      If 1000 tweets is sufficient, use a simple search that just calls twitterSearch once
      If more tweets exist (in past week), after calling twitterSearch,
        use the getEarliestID function to get earliest id so far,
        and call twitterSearch again with the maxID parameter to get even earlier tweets
'''

# code for twitterSearch adapted from Matt Russell, Mining Social Web, ed. 2, Chapter 9
import twitter
import json
import sys
from datetime import datetime


# twitter search api to repeatedly get a custom query
#  the kw parameter allows additional keyword arguments
# see the twitter api docs for additional search criteria that can be used
# arguments:  the twitter_api object from oauth_login
#             the query string
#             the max_results argument defaults to 20
#             other keyword arguments
# results:   a list of tweets - called "statuses" from Twitter

def twitterSearch(twitter_api, query, max_results=20, **kw):
  # see https://dev.twitter.com/docs/api/1.1/get/search/tweets
  # the first search initializes a cursor, stored in the metadata results,
  #   that allows next searches to return additional tweets
  search_results = twitter_api.search.tweets(q=query, count=100, **kw)
  
  # get the tweets from the results
  statuses = search_results['statuses']
  
  # Iterate through batches of results by following the cursor until we
  #  reach the desired number of results, keeping in mind that OAuth users
  #  can "only" make 100 search queries per 15 minute interval.
  #  See https://dev.twitter.com/docs/rate-limiting/1.1/limits  for details.
  #  A reasonable number of results is ~1000, even though that many
  #  may not exist (for the past week) for some queries.
  
  # Limit the results to the minimum of the requested max and 1000
  max_results = min(1000, max_results)
  
  # a for loop that executes up to 10 times (10 * 100 = 1000)
  for i in range(9):   # i is not actually used, this just counts
    try:
      next_results = search_results['search_metadata']['next_results']
    except KeyError:
      # no more results when next_results doesn't exist as a key
      break
    # Create a dictionary from next_results that will give kw args to next search
    kwargs = dict([kv.split('=') for kv in next_results[1:].split('&') ])
    # get the next search results and add the tweets to the statuses list
    #  (**kwargs is the python that "unpacks" the kwargs dict to be the keyword parameters)
    search_results = twitter_api.search.tweets(**kwargs)
    # get just the statuses, ignoring metadata
    statuses += search_results['statuses']
    # if the number of tweets is over the limit, quit
    if len(statuses) > max_results:
      break
  # returns the list of tweets
  return statuses

# this function finds the earliest tweet id in a list of tweets
#   the result can be used as the keyword max_id argument to a search
# Parameter:  list of tweets/statuses, here the tweets are called docs
# Result:  tweet id of (one of) the earliest tweets by date and time
def getEarliestID(doclist):
  # find one of the lowest ids to use as the new max_id
  datetweets = {}

  for doc in doclist:
    # get the tweetid from the keys
    docID = doc['id']
    # get the date string
    datestr = doc['created_at']
    # convert the key string to a datetime object
    # twitter date strings have 2 different formats, one of them contains a comma
    if ',' in datestr:
        dt = datetime.strptime(datestr, "%a, %d %b %Y %H:%M:%S +0000")
    else:
        dt = datetime.strptime(datestr, "%a %b %d %H:%M:%S +0000 %Y")
    # use the datetime object as a dictionary key
    if not dt in datetweets.keys():
        datetweets[dt] = [docID]
    # otherwise add it to the tweet id list
    else:
        datetweets[dt].append(docID)

  if not len(datetweets.keys())==0:
    # sort the keys by the datetime object
    sortedkeys = sorted(datetweets.keys())

    # the new max id will be the first of the earliest
    maxID = datetweets[sortedkeys[0]][0]
    # the date will be the first key in the sorted order
    print ("First Date Time = ", sortedkeys[0], " max id =", maxID)
    first = sortedkeys[0]
  else:
    maxID = 0
    first = None
  return (maxID, first )
  

# this set of functions has no test main, instead use twitter_simple_search
  
  