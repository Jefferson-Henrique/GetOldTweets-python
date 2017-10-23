class TweetCriteria:
	
	def __init__(self):
		self.maxTweets = 0
		self.within = "15mi"
		
	def setUsername(self, username):
		self.username = username
		return self
		
	def setSince(self, since):
		self.since = since
		return self
	
	def setUntil(self, until):
		self.until = until
		return self
		
	def setQuerySearch(self, querySearch):
		self.querySearch = querySearch
		return self
		
	def setMaxTweets(self, maxTweets):
		self.maxTweets = maxTweets
		return self

	def setTopTweets(self, topTweets):
		self.topTweets = topTweets
		return self
	
	def setNear(self, near):
		self.near = near
		return self

	def setWithin(self, within):
		self.within = within
		return self

	def setLang(self, lang):
		self.lang = lang
		return lang
