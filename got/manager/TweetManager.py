import urllib.request, urllib.parse, urllib.error,urllib.request,urllib.error,urllib.parse,json,re,datetime,sys,http.cookiejar
from .. import models
from pyquery import PyQuery

class TweetManager:
	
	def __init__(self):
		pass
		
	@staticmethod
	def getTweets(tweetCriteria, receiveBuffer=None, bufferLength=100, proxy=None):
		refreshCursor = ''
	
		results = []
		resultsAux = []
		cookieJar = http.cookiejar.CookieJar()

		active = True

		while active:
			json = TweetManager.getJsonReponse(tweetCriteria, refreshCursor, cookieJar, proxy)
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
				txt = re.sub(r"\s+", " ", tweetPQ("p.js-tweet-text").text().replace('# ', '#').replace('@ ', '@'));
				retweets = int(tweetPQ("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""));
				favorites = int(tweetPQ("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""));
				dateSec = int(tweetPQ("small.time span.js-short-timestamp").attr("data-time"));
				id = tweetPQ.attr("data-tweet-id");
				permalink = tweetPQ.attr("data-permalink-path");
				user_id = int(tweetPQ("a.js-user-profile-link").attr("data-user-id"))
				
				geo = ''
				geoSpan = tweetPQ('span.Tweet-geo')
				if len(geoSpan) > 0:
					geo = geoSpan.attr('title')
				urls = []
				for link in tweetPQ("a"):
					try:
						urls.append((link.attrib["data-expanded-url"]))
					except KeyError:
						pass
				tweet.id = id
				tweet.permalink = 'https://twitter.com' + permalink
				tweet.username = usernameTweet
				
				tweet.text = txt
				tweet.date = datetime.datetime.fromtimestamp(dateSec)
				tweet.formatted_date = datetime.datetime.fromtimestamp(dateSec).strftime("%a %b %d %X +0000 %Y")
				tweet.retweets = retweets
				tweet.favorites = favorites
				tweet.mentions = " ".join(re.compile('(@\\w*)').findall(tweet.text))
				tweet.hashtags = " ".join(re.compile('(#\\w*)').findall(tweet.text))
				tweet.geo = geo
				tweet.urls = ",".join(urls)
				tweet.author_id = user_id
				
				results.append(tweet)
				resultsAux.append(tweet)
				
				if receiveBuffer and len(resultsAux) >= bufferLength:
					receiveBuffer(resultsAux)
					resultsAux = []
				
				if tweetCriteria.maxTweets > 0 and len(results) >= tweetCriteria.maxTweets:
					active = False
					break
					
		
		if receiveBuffer and len(resultsAux) > 0:
			receiveBuffer(resultsAux)
		
		return results
	
	@staticmethod
	def getJsonReponse(tweetCriteria, refreshCursor, cookieJar, proxy):
		url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&%s&src=typd&max_position=%s"
		urlGetData = ''
		
		if hasattr(tweetCriteria, 'querySearch'):
			urlGetData += tweetCriteria.querySearch + ' '

		if hasattr(tweetCriteria, 'exactSearch'):
			urlGetData += '"' + tweetCriteria.exactSearch + '" '

		if hasattr(tweetCriteria, 'anySearch'):
			temp_list = tweetCriteria.anySearch.split()
			if (len(temp_list) == 1):
				urlGetData += temp_list[0] + ' '
			else:
				for w in temp_list:
					urlGetData += w
					if (w != temp_list[-1]):
						urlGetData += ' OR '
				urlGetData += ' '

		if hasattr(tweetCriteria, 'excludeSearch'):
			urlGetData += '-' + tweetCriteria.excludeSearch + ' '

		if hasattr(tweetCriteria, 'hashtag'):
				temp_list = tweetCriteria.hashtag.split()
				if (len(temp_list) == 1):
					urlGetData += '#' + temp_list[0] + ' '
				else:
					for h in temp_list:
						urlGetData += '#' + h
						if (h != temp_list[-1]):
							urlGetData += ' OR '
					urlGetData += ' '

		if hasattr(tweetCriteria, 'author'):
			temp_list = tweetCriteria.author.split()
			if (len(temp_list) == 1):
				urlGetData += 'from:' + temp_list[0] + ' '
			else:
				for usr in temp_list:
					urlGetData += 'from:' + usr
					if (usr != temp_list[-1]):
						urlGetData += ' OR '
				urlGetData += ' '
			
		if hasattr(tweetCriteria, 'recipient'):
			temp_list = tweetCriteria.recipient.split()
			if (len(temp_list) == 1):
				urlGetData += 'to:' + temp_list[0] + ' '
			else:
				for usr in temp_list:
					urlGetData += 'to:' + usr
					if (usr != temp_list[-1]):
						urlGetData += ' OR '
				urlGetData += ' '

		if hasattr(tweetCriteria, 'mention'):
			temp_list = tweetCriteria.mention.split()
			if (len(temp_list) == 1):
				urlGetData += '@' + temp_list[0] + ' '
			else:
				for usr in temp_list:
					urlGetData += '@' + usr
					if (usr != temp_list[-1]):
						urlGetData += ' OR '
				urlGetData += ' '

		if hasattr(tweetCriteria, 'location'):
			urlGetData += 'near:"' + tweetCriteria.location + '" within:' + str(tweetCriteria.radius) + ' '

		if hasattr(tweetCriteria, 'since'):
			urlGetData += 'since:' + tweetCriteria.since + ' '
			
		if hasattr(tweetCriteria, 'until'):
			urlGetData += 'until:' + tweetCriteria.until + ' '
			
		if hasattr(tweetCriteria, 'lang'):
			urlLang = 'lang=' + tweetCriteria.lang
		else:
			urlLang = 'lang=en'
		
		url = url % (urllib.parse.quote(urlGetData), urlLang, refreshCursor)
		#print(tweetCriteria.exactSearch)
		print("Try to see on browser: https://twitter.com/search?q=%s&src=typd" % urllib.parse.quote(urlGetData))

		headers = [
			('Host', "twitter.com"),
			('User-Agent', "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"),
			('Accept', "application/json, text/javascript, */*; q=0.01"),
			('Accept-Language', "de,en-US;q=0.7,en;q=0.3"),
			('X-Requested-With', "XMLHttpRequest"),
			('Referer', url),
			('Connection', "keep-alive")
		]

		if proxy:
			opener = urllib.request.build_opener(urllib.request.ProxyHandler({'http': proxy, 'https': proxy}), urllib.request.HTTPCookieProcessor(cookieJar))
		else:
			opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookieJar))
		opener.addheaders = headers

		try:
			response = opener.open(url)
			jsonResponse = response.read()
		except:
			#print("Twitter weird response. Try to see on browser: ", url)
			print("Twitter weird response. Try to see on browser: https://twitter.com/search?q=%s&src=typd" % urllib.parse.quote(urlGetData))
			print("Unexpected error:", sys.exc_info()[0])
			sys.exit()
			return
		
		dataJson = json.loads(jsonResponse.decode())
		
		return dataJson		