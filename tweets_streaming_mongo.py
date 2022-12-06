# Import the necessary libaries:

from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient
 
MONGO_HOST= 'mongodb://localhost:27017/vaccinedb'  # The first step required to run this program is you need to make a path on your computer
# as well as a database in mongo DB in order to store the scraped tweets.
#For example, if you wanted to monitor what people are saying about specific vaccine companies:
 
WORDS = ['moderna','Moderna', 'pfizer','Pfizer', 'johnson and johnson', 'Johnson and Johnson']   # Next, the WORDS variable is the part where you put in all of the keywords that you want collected.

 
CONSUMER_KEY= '' # Type in your consumer key from the twitter api here
CONSUMER_SECRET= '' # Type in the consumer secret key from the twitter api here
ACCESS_TOKEN= '' # Type in the access token from the twitter api here
ACCESS_TOKEN_SECRET= '' # Type in the secret access token from the twitter api here
 
#StreamListener is a class provided by tweepy to access the Twitter Streaming API:    
    

class StreamListener(tweepy.StreamListener):
 
    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")
 
    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False
 
    def on_data(self, data):
        #This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
            client = MongoClient(MONGO_HOST)
            
            # Use twitterdb database. If it doesn't exist, it will be created.
            db = client.vaccinedb
    
            # Decode the JSON from Twitter
            datajson = json.loads(data)
            
            #grab the 'created_at' data from the Tweet to use for display
            created_at = datajson['created_at']
 
            #print out a message to the screen that we have collected a tweet
            print("Tweet collected at " + str(created_at))
            
            #insert the data into a collection called vaccine_tweets
            #if vaccine_tweets doesn't exist, it will be created.
            db.vaccine_tweets.insert(datajson)
        except Exception as e:
           print(e)
 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET) # Part of the code that will authorize consumer twitter api credentials
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET) # Part of the code that will authorize access twitter api credentials

while True:
    try:
        #Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
        listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True)) 
        streamer = tweepy.Stream(auth=auth, listener=listener)
        print("Tracking: " + str(WORDS))
        streamer.filter(track=WORDS)
    except:
        # try after one minute if fails
        time.sleep(60)
