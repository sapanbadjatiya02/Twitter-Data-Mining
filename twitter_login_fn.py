''' Provides function that connects to twitter
    Usage is shown in main test program
'''

import twitter

# login to Twitter to gain access to your own account
def oauth_login():
  # put the authorization codes here from your twitter developer application
  CONSUMER_KEY = ''
  CONSUMER_SECRET = ''
  OAUTH_TOKEN = ''
  OAUTH_SECRET = ''
  
  # get the authorization from Twitter and save in the twitter package
  auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
  twitter_api = twitter.Twitter(auth=auth)
  # return the twitter api object that allows access for the twitter api functions
  return twitter_api
    
# Test program to show how to connect
if __name__ == '__main__':
  twitter_api = oauth_login()
  print ("Twitter OAuthorization: ", twitter_api)