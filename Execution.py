import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
import json
import time
import sys,getopt,datetime,codecs
import sys
import Main
if sys.version_info[0] < 3:
    import got
else:
    import got3 as got
import pandas as pd
class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self):

        # input for term to be searched and how many tweets to search
        searchTerm = input("Enter Keywords (Space Seperated): ")
        NoOfTerms = int(input("Enter how many tweets to search: "))
        start=input("Enter Start date in format YYYY-MM-DD: ")
        end=input("Enter End date in format YYYY-MM-DD: ")
        loc=input("Enter Location: ")
        
        # searching for tweets
        #self.tweets = tweepy.Cursor(api.search, q=searchTerm, since=start, untill=end, lang = "en").items(NoOfTerms)

        tweetCriteria = got.manager.TweetCriteria().setNear(loc).setQuerySearch(searchTerm).setSince(start).setUntil(end).setMaxTweets(NoOfTerms)
        self.tweets =  (got.manager.TweetManager.getTweets(tweetCriteria))
	
	# Open/create a file to append data to
        csvFile = codecs.open("output_got3.csv", "a", "utf-8")
        res=[]

        # Use csv writer
        csvWriter = csv.writer(csvFile)

        # creating some variables to store info
        polarity = 0
        positive = 0
        negative = 0
        neutral = 0

        csvWriter.writerow(["Date and Time Created","User Name","Tweet for "+str(searchTerm),"Response"])
        
        # iterating through tweets fetched
        for tweet in self.tweets:
            #Append to temp so that we can store in csv later. I use encode UTF-8
            
            #print (tweet.text.translate(tweet.text))    #print tweet's text
            analysis = TextBlob(tweet.text)
            #print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
                f=0
            elif (analysis.sentiment.polarity > 0):
                positive +=1
                f=1
            elif (analysis.sentiment.polarity < 0):
                negative +=1
                f=-1
            
            #csvFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (tweet.username, tweet.date.strftime("%Y-%m-%d %H:%M"), tweet.retweets, tweet.favorites, tweet.text, tweet.geo, tweet.mentions, tweet.hashtags, tweet.id, tweet.permalink)))

            #csvFile.write(('\n%s;%s;%s;' % (tweet.username, tweet.date.strftime("%Y-%m-%d %H:%M"),tweet.text)))
            csvWriter.writerow((tweet.date.strftime("%Y-%m-%d %H:%M"),tweet.username,tweet.text,str(f)))
            csvFile.flush()
            # Write to csv and close csv file
            #csvWriter.writerow(tweet.text)
            #csvWriter.writerow([tweet.created_at,tweet.user.screen_name, self.cleanTweet(tweet.text).encode('utf-8')])
        csvFile.close()
        #print(res)
        # finding average of how people are reacting
        positive = self.percentage(positive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)

        # finding average reaction
        polarity = polarity / NoOfTerms

        # printing out data
        print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
        print()
        print("General Report: ")

        if (polarity == 0):
            print("Neutral")
        elif (polarity > 0):
            print("Positive")
        elif (polarity <0):
            print("Negative")

        print()
        print("Detailed Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(negative) + "% people thought it was negative")
        print(str(neutral) + "% people thought it was neutral")

       #self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)


    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData()
