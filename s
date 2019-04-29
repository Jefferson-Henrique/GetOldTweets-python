[1mdiff --git a/Exporter.py b/Exporter.py[m
[1mindex 254bdda..913c47c 100644[m
[1m--- a/Exporter.py[m
[1m+++ b/Exporter.py[m
[36m@@ -1,79 +1,97 @@[m
 # -*- coding: utf-8 -*-[m
[31m-import sys,getopt,datetime,codecs[m
[32m+[m[32mimport sys, getopt, datetime, codecs, csv[m
[32m+[m
 if sys.version_info[0] < 3:[m
     import got[m
 else:[m
     import got3 as got[m
 [m
[31m-def main(argv):[m
[31m-[m
[31m-	if len(argv) == 0:[m
[31m-		print('You must pass some parameters. Use \"-h\" to help.')[m
[31m-		return[m
[31m-[m
[31m-	if len(argv) == 1 and argv[0] == '-h':[m
[31m-		f = open('exporter_help_text.txt', 'r')[m
[31m-		print f.read()[m
[31m-		f.close()[m
[31m-[m
[31m-		return[m
[31m-[m
[31m-	try:[m
[31m-		opts, args = getopt.getopt(argv, "", ("username=", "near=", "within=", "since=", "until=", "querysearch=", "toptweets", "maxtweets=", "output="))[m
[31m-[m
[31m-		tweetCriteria = got.manager.TweetCriteria()[m
[31m-		outputFileName = "output_got.csv"[m
[31m-[m
[31m-		for opt,arg in opts:[m
[31m-			if opt == '--username':[m
[31m-				tweetCriteria.username = arg[m
[31m-[m
[31m-			elif opt == '--since':[m
[31m-				tweetCriteria.since = arg[m
[31m-[m
[31m-			elif opt == '--until':[m
[31m-				tweetCriteria.until = arg[m
 [m
[31m-			elif opt == '--querysearch':[m
[31m-				tweetCriteria.querySearch = arg[m
[31m-[m
[31m-			elif opt == '--toptweets':[m
[31m-				tweetCriteria.topTweets = True[m
[31m-[m
[31m-			elif opt == '--maxtweets':[m
[31m-				tweetCriteria.maxTweets = int(arg)[m
[31m-			[m
[31m-			elif opt == '--near':[m
[31m-				tweetCriteria.near = '"' + arg + '"'[m
[31m-			[m
[31m-			elif opt == '--within':[m
[31m-				tweetCriteria.within = '"' + arg + '"'[m
[31m-[m
[31m-			elif opt == '--within':[m
[31m-				tweetCriteria.within = '"' + arg + '"'[m
[31m-[m
[31m-			elif opt == '--output':[m
[31m-				outputFileName = arg[m
[31m-				[m
[31m-		outputFile = codecs.open(outputFileName, "w+", "utf-8")[m
[31m-[m
[31m-		outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')[m
[31m-[m
[31m-		print('Searching...\n')[m
[31m-[m
[31m-		def receiveBuffer(tweets):[m
[31m-			for t in tweets:[m
[31m-				outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink)))[m
[31m-			outputFile.flush()[m
[31m-			print('More %d saved on file...\n' % len(tweets))[m
[31m-[m
[31m-		got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)[m
[32m+[m[32mdef main(argv):[m
[32m+[m[32m    if len(argv) == 0:[m
[32m+[m[32m        print('You must pass some parameters. Use \"-h\" to help.')[m
[32m+[m[32m        return[m
[32m+[m
[32m+[m[32m    if len(argv) == 1 and argv[0] == '-h':[m
[32m+[m[32m        f = open('exporter_help_text.txt', 'r')[m
[32m+[m[32m        print(f.read())[m
[32m+[m[32m        f.close()[m
[32m+[m
[32m+[m[32m        return[m
[32m+[m
[32m+[m[32m    try:[m
[32m+[m[32m        opts, args = getopt.getopt(argv, "", ([m
[32m+[m[32m        "username=", "near=", "within=", "since=", "until=", "querysearch=", "toptweets", "maxtweets=", "output=", "lang="))[m
[32m+[m
[32m+[m[32m        tweetCriteria = got.manager.TweetCriteria()[m
[32m+[m[32m        outputFileName = "output_got.csv"[m
[32m+[m
[32m+[m[32m        for opt, arg in opts:[m
[32m+[m[32m            if opt == '--username':[m
[32m+[m[32m                tweetCriteria.username = arg[m
[32m+[m
[32m+[m[32m            elif opt == '--since':[m
[32m+[m[32m                tweetCriteria.since = arg[m
[32m+[m
[32m+[m[32m            elif opt == '--until':[m
[32m+[m[32m                tweetCriteria.until = arg[m
[32m+[m
[32m+[m[32m            elif opt == '--querysearch':[m
[32m+[m[32m                tweetCriteria.querySearch = arg[m
[32m+[m
[32m+[m[32m            elif opt == '--toptweets':[m
[32m+[m[32m                tweetCriteria.topTweets = True[m
[32m+[m
[32m+[m[32m            elif opt == '--maxtweets':[m
[32m+[m[32m                tweetCriteria.maxTweets = int(arg)[m
[32m+[m
[32m+[m[32m            elif opt == '--near':[m
[32m+[m[32m                tweetCriteria.near = '"' + arg + '"'[m
[32m+[m
[32m+[m[32m            elif opt == '--within':[m
[32m+[m[32m                tweetCriteria.within = '"' + arg + '"'[m
[32m+[m
[32m+[m[32m            elif opt == '--output':[m
[32m+[m[32m                outputFileName = arg[m
[32m+[m
[32m+[m[32m            elif opt == '--lang':[m
[32m+[m[32m                tweetCriteria.lang = arg[m
[32m+[m
[32m+[m[32m        outputFile = csv.writer(open(outputFileName, "w"), encoding='utf-8-sig', delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)[m
[32m+[m[41m        [m
[32m+[m[32m        outputFile.writerow([m
[32m+[m[32m            # ['username','date','retweets','favorites','text','mentions','hashtags','id','permalink', 'emoji'])[m
[32m+[m[32m            ['username','date','retweets','favorites','text','geo','mentions','hashtags','id','permalink', 'emoji'])[m
[32m+[m[41m        [m
[32m+[m[32m        print('Collecting tweets...\n')[m
[32m+[m
[32m+[m[32m        def receiveBuffer(tweets):[m
[32m+[m[32m            for t in tweets:[m
[32m+[m[32m                print("> Tweets :" + t.text + "\n\n")[m
[32m+[m[32m                add_list = [][m
[32m+[m[32m                if (isinstance(t.emojis, list)):[m
[32m+[m[32m                    emoji = ' '.join(t.emojis)[m
[32m+[m[32m                else:[m
[32m+[m[32m                    emoji = t.emojis[m
[32m+[m[32m                for each in [t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.mentions, t.hashtags, t.id, t.permalink, emoji]:[m
[32m+[m[32m                    if type(each) is str:[m
[32m+[m[32m                        valid_s = ''[m
[32m+[m[32m                        for ch in each:[m
[32m+[m[32m                            if ord(ch) in range(128):[m
[32m+[m[32m                                valid_s+=ch[m
[32m+[m[32m                        add_list.append(valid_s)[m
[32m+[m[32m                    else:[m
[32m+[m[32m                        add_list.append(each)[m
[32m+[m[32m                outputFile.writerow(add_list)[m
[32m+[m[32m            print('%d tweets saved on file...\n' % len(tweets))[m
[32m+[m
[32m+[m[32m        got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)[m
[32m+[m
[32m+[m[32m    except arg:[m
[32m+[m[32m        print('Arguments parse error, try -h' + arg)[m
[32m+[m[32m    finally:[m
[32m+[m[32m        print('Done. Output file generated "%s".' % outputFileName)[m
 [m
[31m-	except arg:[m
[31m-		print('Arguments parser error, try -h' + arg)[m
[31m-	finally:[m
[31m-		outputFile.close()[m
[31m-		print('Done. Output file generated "%s".' % outputFileName)[m
 [m
 if __name__ == '__main__':[m
[31m-	main(sys.argv[1:])[m
[32m+[m[32m    main(sys.argv[1:])[m
[1mdiff --git a/Main.py b/Main.py[m
[1mindex 75496a5..a348b3a 100644[m
[1m--- a/Main.py[m
[1m+++ b/Main.py[m
[36m@@ -1,11 +1,10 @@[m
 import sys[m
 if sys.version_info[0] < 3:[m
[31m-    import got[m
[32m+[m	[32mimport got[m
 else:[m
[31m-    import got3 as got[m
[32m+[m	[32mimport got3 as got[m
 [m
 def main():[m
[31m-[m
 	def printTweet(descr, t):[m
 		print(descr)[m
 		print("Username: %s" % t.username)[m
[36m@@ -15,22 +14,22 @@[m [mdef main():[m
 		print("Hashtags: %s\n" % t.hashtags)[m
 [m
 	# Example 1 - Get tweets by username[m
[31m-	tweetCriteria = got.manager.TweetCriteria().setUsername('barackobama').setMaxTweets(1)[m
[31m-	tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0][m
[31m-[m
[31m-	printTweet("### Example 1 - Get tweets by username [barackobama]", tweet)[m
[31m-[m
[31m-	# Example 2 - Get tweets by query search[m
[31m-	tweetCriteria = got.manager.TweetCriteria().setQuerySearch('europe refugees').setSince("2015-05-01").setUntil("2015-09-30").setMaxTweets(1)[m
[31m-	tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0][m
[31m-[m
[31m-	printTweet("### Example 2 - Get tweets by query search [europe refugees]", tweet)[m
[31m-[m
[31m-	# Example 3 - Get tweets by username and bound dates[m
[31m-	tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama").setSince("2015-09-10").setUntil("2015-09-12").setMaxTweets(1)[m
[31m-	tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0][m
[31m-[m
[31m-	printTweet("### Example 3 - Get tweets by username and bound dates [barackobama, '2015-09-10', '2015-09-12']", tweet)[m
[32m+[m	[32m# tweetCriteria = got.manager.TweetCriteria().setUsername('barackobama').setMaxTweets(1)[m
[32m+[m	[32m# tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0][m
[32m+[m	[32m#[m
[32m+[m	[32m# printTweet("### Example 1 - Get tweets by username [barackobama]", tweet)[m
[32m+[m	[32m#[m
[32m+[m	[32m# # Example 2 - Get tweets by query search[m
[32m+[m	[32m# tweetCriteria = got.manager.TweetCriteria().setQuerySearch('europe refugees').setSince("2015-05-01").setUntil("2015-09-30").setMaxTweets(1)[m
[32m+[m	[32m# tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0][m
[32m+[m	[32m#[m
[32m+[m	[32m# printTweet("### Example 2 - Get tweets by query search [europe refugees]", tweet)[m
[32m+[m	[32m#[m
[32m+[m	[32m# # Example 3 - Get tweets by username and bound dates[m
[32m+[m	[32m# tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama").setSince("2015-09-10").setUntil("2015-09-12").setMaxTweets(1)[m
[32m+[m	[32m# tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0][m
[32m+[m	[32m#[m
[32m+[m	[32m# printTweet("### Example 3 - Get tweets by username and bound dates [barackobama, '2015-09-10', '2015-09-12']", tweet)[m
 [m
 if __name__ == '__main__':[m
 	main()[m
[1mdiff --git a/got3/manager/TweetCriteria.py b/got3/manager/TweetCriteria.py[m
[1mindex 695462b..286d3d7 100644[m
[1m--- a/got3/manager/TweetCriteria.py[m
[1m+++ b/got3/manager/TweetCriteria.py[m
[36m@@ -1,32 +1,40 @@[m
 class TweetCriteria:[m
 [m
[31m-	def __init__(self):[m
[31m-		self.maxTweets = 0[m
[32m+[m[32m    def __init__(self):[m
[32m+[m[32m        self.maxTweets = 0[m
 [m
[31m-	def setUsername(self, username):[m
[31m-		self.username = username[m
[31m-		return self[m
[32m+[m[32m    def setUsername(self, username):[m
[32m+[m[32m        self.username = username[m
[32m+[m[32m        return self[m
 [m
[31m-	def setSince(self, since):[m
[31m-		self.since = since[m
[31m-		return self[m
[32m+[m[32m    def setSince(self, since):[m
[32m+[m[32m        self.since = since[m
[32m+[m[32m        return self[m
 [m
[31m-	def setUntil(self, until):[m
[31m-		self.until = until[m
[31m-		return self[m
[32m+[m[32m    def setUntil(self, until):[m
[32m+[m[32m        self.until = until[m
[32m+[m[32m        return self[m
 [m
[31m-	def setQuerySearch(self, querySearch):[m
[31m-		self.querySearch = querySearch[m
[31m-		return self[m
[32m+[m[32m    def setQuerySearch(self, querySearch):[m
[32m+[m[32m        self.querySearch = querySearch[m
[32m+[m[32m        return self[m
 [m
[31m-	def setMaxTweets(self, maxTweets):[m
[31m-		self.maxTweets = maxTweets[m
[31m-		return self[m
[32m+[m[32m    def setMaxTweets(self, maxTweets):[m
[32m+[m[32m        self.maxTweets = maxTweets[m
[32m+[m[32m        return self[m
 [m
[31m-	def setLang(self, Lang):[m
[31m-		self.lang = Lang[m
[31m-		return self[m
[32m+[m[32m    def setLang(self, Lang):[m
[32m+[m[32m        self.lang = Lang[m
[32m+[m[32m        return self[m
 [m
[31m-	def setTopTweets(self, topTweets):[m
[31m- 		self.topTweets = topTweets[m
[31m- 		return self[m
\ No newline at end of file[m
[32m+[m[32m    def setTopTweets(self, topTweets):[m
[32m+[m[32m        self.topTweets = topTweets[m
[32m+[m[32m        return self[m
[32m+[m
[32m+[m[32m    def setNear(self, near):[m
[32m+[m[32m        self.near = near[m
[32m+[m[32m        return self[m
[32m+[m
[32m+[m[32m    def setWithin(self, within):[m
[32m+[m[32m        self.within = within[m
[32m+[m[32m        return self[m
\ No newline at end of file[m
[1mdiff --git a/got3/manager/TweetManager.py b/got3/manager/TweetManager.py[m
[1mindex 7f75bd3..494ec14 100644[m
[1m--- a/got3/manager/TweetManager.py[m
[1m+++ b/got3/manager/TweetManager.py[m
[36m@@ -3,139 +3,153 @@[m [mfrom .. import models[m
 from pyquery import PyQuery[m
 [m
 class TweetManager:[m
[31m-	[m
[31m-	def __init__(self):[m
[31m-		pass[m
[31m-		[m
[31m-	@staticmethod[m
[31m-	def getTweets(tweetCriteria, receiveBuffer=None, bufferLength=100, proxy=None):[m
[31m-		refreshCursor = ''[m
[31m-	[m
[31m-		results = [][m
[31m-		resultsAux = [][m
[31m-		cookieJar = http.cookiejar.CookieJar()[m
[32m+[m[41m    [m
[32m+[m[32m    def __init__(self):[m[41m[m
[32m+[m[32m        pass[m[41m[m
[32m+[m[41m        [m
[32m+[m[32m    @staticmethod[m[41m[m
[32m+[m[32m    def getTweets(tweetCriteria, receiveBuffer=None, bufferLength=100, proxy=None):[m[41m[m
[32m+[m[32m        refreshCursor = ''[m[41m[m
[32m+[m[41m    [m
[32m+[m[32m        results = [][m[41m[m
[32m+[m[32m        resultsAux = [][m[41m[m
[32m+[m[32m        cookieJar = http.cookiejar.CookieJar()[m[41m[m
 [m
[31m-		active = True[m
[32m+[m[32m        active = True[m[41m[m
 [m
[31m-		while active:[m
[31m-			json = TweetManager.getJsonReponse(tweetCriteria, refreshCursor, cookieJar, proxy)[m
[31m-			if len(json['items_html'].strip()) == 0:[m
[31m-				break[m
[32m+[m[32m        while active:[m[41m[m
[32m+[m[32m            json = TweetManager.getJsonReponse(tweetCriteria, refreshCursor, cookieJar, proxy)[m[41m[m
[32m+[m[32m            if len(json['items_html'].strip()) == 0:[m[41m[m
[32m+[m[32m                break[m[41m[m
 [m
[31m-			refreshCursor = json['min_position'][m
[31m-			scrapedTweets = PyQuery(json['items_html'])[m
[31m-			#Remove incomplete tweets withheld by Twitter Guidelines[m
[31m-			scrapedTweets.remove('div.withheld-tweet')[m
[31m-			tweets = scrapedTweets('div.js-stream-tweet')[m
[31m-			[m
[31m-			if len(tweets) == 0:[m
[31m-				break[m
[31m-			[m
[31m-			for tweetHTML in tweets:[m
[31m-				tweetPQ = PyQuery(tweetHTML)[m
[31m-				tweet = models.Tweet()[m
[31m-				[m
[31m-				usernameTweet = tweetPQ("span.username.js-action-profile-name b").text()[m
[31m-				txt = re.sub(r"\s+", " ", tweetPQ("p.js-tweet-text").text().replace('# ', '#').replace('@ ', '@'))[m
[31m-				retweets = int(tweetPQ("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""))[m
[31m-				favorites = int(tweetPQ("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""))[m
[31m-				dateSec = int(tweetPQ("small.time span.js-short-timestamp").attr("data-time"))[m
[31m-				id = tweetPQ.attr("data-tweet-id")[m
[31m-				permalink = tweetPQ.attr("data-permalink-path")[m
[31m-				user_id = int(tweetPQ("a.js-user-profile-link").attr("data-user-id"))[m
[31m-				[m
[31m-				geo = ''[m
[31m-				geoSpan = tweetPQ('span.Tweet-geo')[m
[31m-				if len(geoSpan) > 0:[m
[31m-					geo = geoSpan.attr('title')[m
[31m-				urls = [][m
[31m-				for link in tweetPQ("a"):[m
[31m-					try:[m
[31m-						urls.append((link.attrib["data-expanded-url"]))[m
[31m-					except KeyError:[m
[31m-						pass[m
[31m-				tweet.id = id[m
[31m-				tweet.permalink = 'https://twitter.com' + permalink[m
[31m-				tweet.username = usernameTweet[m
[31m-				[m
[31m-				tweet.text = txt[m
[31m-				tweet.date = datetime.datetime.fromtimestamp(dateSec)[m
[31m-				tweet.formatted_date = datetime.datetime.fromtimestamp(dateSec).strftime("%a %b %d %X +0000 %Y")[m
[31m-				tweet.retweets = retweets[m
[31m-				tweet.favorites = favorites[m
[31m-				tweet.mentions = " ".join(re.compile('(@\\w*)').findall(tweet.text))[m
[31m-				tweet.hashtags = " ".join(re.compile('(#\\w*)').findall(tweet.text))[m
[31m-				tweet.geo = geo[m
[31m-				tweet.urls = ",".join(urls)[m
[31m-				tweet.author_id = user_id[m
[31m-				[m
[31m-				results.append(tweet)[m
[31m-				resultsAux.append(tweet)[m
[31m-				[m
[31m-				if receiveBuffer and len(resultsAux) >= bufferLength:[m
[31m-					receiveBuffer(resultsAux)[m
[31m-					resultsAux = [][m
[31m-				[m
[31m-				if tweetCriteria.maxTweets > 0 and len(results) >= tweetCriteria.maxTweets:[m
[31m-					active = False[m
[31m-					break[m
[31m-					[m
[31m-		[m
[31m-		if receiveBuffer and len(resultsAux) > 0:[m
[31m-			receiveBuffer(resultsAux)[m
[31m-		[m
[31m-		return results[m
[31m-	[m
[31m-	@staticmethod[m
[31m-	def getJsonReponse(tweetCriteria, refreshCursor, cookieJar, proxy):[m
[31m-		url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&%smax_position=%s"[m
[31m-		[m
[31m-		urlGetData = ''[m
[31m-		if hasattr(tweetCriteria, 'username'):[m
[31m-			urlGetData += ' from:' + tweetCriteria.username[m
[31m-			[m
[31m-		if hasattr(tweetCriteria, 'since'):[m
[31m-			urlGetData += ' since:' + tweetCriteria.since[m
[31m-			[m
[31m-		if hasattr(tweetCriteria, 'until'):[m
[31m-			urlGetData += ' until:' + tweetCriteria.until[m
[31m-			[m
[31m-		if hasattr(tweetCriteria, 'querySearch'):[m
[31m-			urlGetData += ' ' + tweetCriteria.querySearch[m
[31m-			[m
[31m-		if hasattr(tweetCriteria, 'lang'):[m
[31m-			urlLang = 'lang=' + tweetCriteria.lang + '&'[m
[31m-		else:[m
[31m-			urlLang = ''[m
[31m-		url = url % (urllib.parse.quote(urlGetData), urlLang, refreshCursor)[m
[31m-		#print(url)[m
[32m+[m[32m            refreshCursor = json['min_position'][m[41m[m
[32m+[m[32m            scrapedTweets = PyQuery(json['items_html'])[m[41m[m
[32m+[m[32m            #Remove incomplete tweets withheld by Twitter Guidelines[m[41m[m
[32m+[m[32m            scrapedTweets.remove('div.withheld-tweet')[m[41m[m
[32m+[m[32m            tweets = scrapedTweets('div.js-stream-tweet')[m[41m[m
[32m+[m[41m            [m
[32m+[m[32m            if len(tweets) == 0:[m[41m[m
[32m+[m[32m                break[m[41m[m
[32m+[m[41m            [m
[32m+[m[32m            for tweetHTML in tweets:[m[41m[m
[32m+[m[32m                tweetPQ = PyQuery(tweetHTML)[m[41m[m
[32m+[m[32m                tweet = models.Tweet()[m[41m[m
[32m+[m[41m                [m
[32m+[m[32m                uTweet = tweetPQ("span.username.u-dir.u-textTruncate b").text()[m[41m[m
[32m+[m[32m                if (' ' in uTweet) == True:[m[41m[m
[32m+[m[32m                    # split and get first index[m[41m[m
[32m+[m[32m                    usernameTweet = uTweet.split(' ')[0][m[41m[m
[32m+[m[32m                else:[m[41m[m
[32m+[m[32m                    usernameTweet = uTweet[m[41m[m
[32m+[m[32m                txt = re.sub(r"\s+", " ", tweetPQ("p.js-tweet-text").text().replace('# ', '#').replace('@ ', '@'))[m[41m[m
[32m+[m[32m                retweets = int(tweetPQ("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""))[m[41m[m
[32m+[m[32m                favorites = int(tweetPQ("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""))[m[41m[m
[32m+[m[32m                dateSec = int(tweetPQ("small.time span.js-short-timestamp").attr("data-time"))[m[41m[m
[32m+[m[32m                id = tweetPQ.attr("data-tweet-id")[m[41m[m
[32m+[m[32m                permalink = tweetPQ.attr("data-permalink-path")[m[41m[m
[32m+[m[32m                user_id = i