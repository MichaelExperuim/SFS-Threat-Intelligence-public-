# This section of code will use snscrape to scrape Twitter for trending tweets and trending hashtags about the Scottsdale Fashion Square Mall.

import snscrape.modules.twitter as sntwitter
from textblob import TextBlob
import datetime

class TwitterProfile:
    
    # Constructor. Takes in a username and creates a TwitterProfile object.
    def __init__(self, username):
        self.username = username # Username of the profile
        self.tweets = [] # List of Tweet objects
        self.hashtags = [] # List of hashtags
        self.bio = "" # Bio of the profile
        self.followers = 0 # Number of followers
        self.url = "" # URL of the profile
        self.verified = False # Boolean value of whether the profile is verified or not
        


class Tweet:
    # Constructor. Takes in a tweet_id, date, content, username, and hashtags and creates a Tweet object.
    def __init__(self, tweet_id, date, content, username, hashtags):
        self.tweet_id = tweet_id
        self.date = date
        self.content = content
        self.username = username
        self.hashtags = hashtags
        
    def sentiment_analysis(self):
    
    
    def search_twitter_profiles():



def main():
    
    # List of all hashtags I want to search for
    hashtags = [
    "#ScottsdaleFashionSquare",
    "#ScottsdaleMall",
    "#ScottsdaleStyle",
    "#ScottsdaleShopping",
    "#FashionSquare",
    "#ScottsdaleFashion",
    "#ShopScottsdale",
    "#FashionMall",
    "#LuxuryShopping",
    "#ArizonaFashion",
    "#SFS"
    ]
    
    # Use snscrape to search for tweets with the hashtags above
    # Calculate start and end dates for the 3-month date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)

    # Convert the dates to string format for the query
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    
    for hashtag in hashtags:
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(hashtag + f' since:{start_date_str} until:{end_date_str}').get_items()):
            if i > 100:
                break
            
            # Create a Tweet object
            tweet_object = Tweet(
                tweet.id, 
                tweet.date, 
                tweet.content, 
                tweet.username, 
                tweet.hashtags
                )
    
    
        

    
    


