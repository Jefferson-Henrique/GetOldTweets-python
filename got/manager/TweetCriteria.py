class TweetCriteria:

	def __init__(self):
		self.maxTweets = 0
		self.radius = 15

	def setQuerySearch(self, querySearch):
			self.querySearch = querySearch
			return self

	def setExactQuerySearch(self, exactSearch):
		self.exactSearch = exactSearch
		return self

	def setAnyQuerySearch(self, anySearch):
		self.anySearch = anySearch
		return self

	def setExcludeQuerySearch(self, excludeSearch):
		self.excludeSearch = excludeSearch
		return self

	def setHashtag(self, hashtag):
		self.hashtag = hashtag
		return self

	def setAuthor(self, author):
		self.author = author
		return self

	def setRecipient(self, recipient):
		self.recipient = recipient
		return self

	def setMention(self, mention):
		self.mention = mention
		return self

	def setNear(self, location):
		self.location = location
		return self

	def setWithin(self, radius):
		self.radius = radius
		return self

	def setSince(self, since):
		self.since = since
		return self

	def setUntil(self, until):
		self.until = until
		return self

	def setLang(self, Lang):
		self.lang = Lang
		return self

	def setMaxTweets(self, maxTweets):
		self.maxTweets = maxTweets
		return self

	def setTopTweets(self, topTweets):
		self.topTweets = topTweets
		return self