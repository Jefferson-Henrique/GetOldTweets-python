# Get Old Tweets Programatically
A project written in Python to get old tweets, it bypass some limitations of Twitter Official API.

![Python 3x](https://img.shields.io/badge/python-3.x-blue.svg)
[![Build Status](https://travis-ci.org/Mottl/GetOldTweets-python3.svg?branch=master)](https://travis-ci.org/Mottl/GetOldTweets-python3)

GetOldTweets-python3 is an improvement fork of the original Jefferson Henrique's [GetOldTweets-python](https://github.com/Jefferson-Henrique/GetOldTweets-python). It fixes issues with **Python 3** and adds features such as searching tweets over multiple users accounts.  
Python 2 support was removed from this fork.

## Details
Twitter Official API has the bother limitation of time constraints, you can't get older tweets than a week. Some tools provide access to older tweets but in the most of them you have to spend some money before.
I was searching other tools to do this job but I didn't found it, so after analyze how Twitter Search through browser works I understand its flow. Basically when you enter on Twitter page a scroll loader starts, if you scroll down you start to get more and more tweets, all through calls to a JSON provider. After mimic we get the best advantage of Twitter Search on browsers, it can search the deepest oldest tweets.

## Prerequisites
Expected package dependencies are listed in the "requirements.txt" file for _pip_, you need to run the following command to get dependencies:
```sh
pip install -r requirements.txt
```

## Components
- **Tweet:** Model class to give some informations about a specific tweet.
  - id (str)
  - permalink (str)
  - username (str)
  - to (str)
  - text (str)
  - date (datetime) in UTC
  - retweets (int)
  - favorites (int)
  - mentions (str)
  - hashtags (str)
  - geo (str)

- **TweetManager:** A manager class to help getting tweets in **Tweet**'s model.
  - getTweets (**TwitterCriteria**): Return the list of tweets retrieved by using an instance of **TwitterCriteria**. 

- **TwitterCriteria:** A collection of search parameters to be used together with **TweetManager**.
  - setUsername (str or iterable): An optional specific username(s) from a twitter account (with or without "@").
  - setSince (str. "yyyy-mm-dd" or "yyyy-mm-dd HH:MM:SS"): A lower bound date/time in UTC to restrict search.
  - setUntil (str. "yyyy-mm-dd" or "yyyy-mm-dd HH:MM:SS"): An upper bound date/time in UTC to restrict search.
  - setQuerySearch (str): A query text to be matched.
  - setTopTweets (bool): If True only the Top Tweets will be retrieved.
  - setNear(str): A reference location area from where tweets were generated.
  - setWithin (str): A distance radius from "near" location (e.g. 15mi).
  - setMaxTweets (int): The maximum number of tweets to be retrieved. If this number is unsetted or lower than 1 all possible tweets will be retrieved.
  
- **Main:** Examples of how to use.

- **Exporter:** Export tweets to a csv file named "output_got.csv".

## Examples of python usage
- Get tweets by username(s)
``` python
tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama whitehouse")\
                                           .setMaxTweets(2)
tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
print tweet.text
```

- Get tweets by query search
``` python
tweetCriteria = got.manager.TweetCriteria().setQuerySearch('europe refugees')\
                                           .setSince("2015-05-01")\
                                           .setUntil("2015-09-30")\
                                           .setMaxTweets(1)
tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
print(tweet.text)
```

- Get tweets by username and bound dates
``` python
tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama")\
                                           .setSince("2015-09-10")\
                                           .setUntil("2015-09-12  23:30:15")\
                                           .setMaxTweets(1)
tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
print(tweet.text)
```

- Get the last 10 top tweets by username
``` python
tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama")\
                                           .setTopTweets(True)\
                                           .setMaxTweets(10)
tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
print(tweet.text)
```

## Examples of a command-line usage
- Get help use:
``` bash
python3 Exporter.py -h
``` 

- Get tweets by username:
``` bash
python3 Exporter.py --username "barackobama" --maxtweets 1
```

- Get tweets by sevaral usernames (use multiple --username options or a comma/space separated list):
``` bash
python3 Exporter.py --username "BarackObama,AngelaMerkeICDU" --username "WhiteHouse"  --maxtweets 1
```
(check https://github.com/Mottl/influencers for some prepared lists of usernames)

- Get top tweets from users specified in files and also specific users:
``` bash
python3 Exporter.py --usernames-from-file userlist.txt --usernames-from-file additinal_list.txt --username "barackobama,whitehouse" --toptweets
```

- Get tweets by a query search:
``` bash
python3 Exporter.py --querysearch "europe refugees" --maxtweets 1
```

- Get tweets by a username and bound dates:
``` bash
python3 Exporter.py --username "barackobama" --since 2015-09-10 --until "2015-09-12 23:30:15" --maxtweets 1
```

- Get the last 10 top tweets by a username:
``` bash
python3 Exporter.py --username "barackobama" --maxtweets 10 --toptweets
```
