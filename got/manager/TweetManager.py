import urllib,urllib2,json,re,datetime
from .. import models
from pyquery import PyQuery

class TweetManager:
	
	def __init__(self):
		pass
		
	@staticmethod
	def getTweets(tweetCriteria):
		refreshCursor = ''
	
		results = []
	
		while True:
			json = TweetManager.getJsonReponse(tweetCriteria, refreshCursor)
			if len(json['items_html'].strip()) == 0:
				break

			refreshCursor = json['min_position']			
			tweets = PyQuery(json['items_html'])('div.js-stream-tweet')
			
			if len(tweets) == 0:
				break
			
			for tweetHTML in tweets:
				tweetPQ = PyQuery(tweetHTML)
				tweet = models.Tweet()
				
				usernameTweet = tweetPQ("span.username.js-action-profile-name b").text();
				txt = re.sub(r"\s+", " ", re.sub(r"[^\x00-\x7F]", "", tweetPQ("p.js-tweet-text").text()).replace('# ', '#').replace('@ ', '@'));
				retweets = int(tweetPQ("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""));
				favorites = int(tweetPQ("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""));
				dateSec = int(tweetPQ("small.time span.js-short-timestamp").attr("data-time"));
				id = tweetPQ.attr("data-tweet-id");
				permalink = tweetPQ.attr("data-permalink-path");
				
				geo = ''
				geoSpan = tweetPQ('span.Tweet-geo')
				if len(geoSpan) > 0:
					geo = geoSpan.attr('title')
				
				tweet.id = id
				tweet.permalink = 'https://twitter.com' + permalink
				tweet.username = usernameTweet
				tweet.text = txt
				tweet.date = datetime.datetime.fromtimestamp(dateSec)
				tweet.retweets = retweets
				tweet.favorites = favorites
				tweet.mentions = " ".join(re.compile('(@\\w*)').findall(tweet.text))
				tweet.hashtags = " ".join(re.compile('(#\\w*)').findall(tweet.text))
				tweet.geo = geo
				
				results.append(tweet)
				
				if tweetCriteria.maxTweets > 0 and len(results) >= tweetCriteria.maxTweets:
					return results
			
		return results
	
	@staticmethod
	def getJsonReponse(tweetCriteria, refreshCursor):
		url = "https://twitter.com/i/search/timeline?f=realtime&q=%s&src=typd&max_position=%s"
		
		urlGetData = ''
		if hasattr(tweetCriteria, 'username'):
			urlGetData += ' from:' + tweetCriteria.username
			
		if hasattr(tweetCriteria, 'since'):
			urlGetData += ' since:' + tweetCriteria.since
			
		if hasattr(tweetCriteria, 'until'):
			urlGetData += ' until:' + tweetCriteria.until
			
		if hasattr(tweetCriteria, 'querySearch'):
			urlGetData += ' ' + tweetCriteria.querySearch
		
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
		
		url = url % (urllib.quote(urlGetData), refreshCursor)
		
		req = urllib2.Request(url, headers = headers)
		
		jsonResponse = urllib2.urlopen(req).read()
		
		dataJson = json.loads(jsonResponse)
		
		return dataJson		