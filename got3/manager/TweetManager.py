import urllib.request
import urllib.parse
import urllib.error
import urllib.request
import urllib.error
import urllib.parse
import json
import re
import datetime
import sys
import http.cookiejar
from pyquery import PyQuery
from bs4 import BeautifulSoup
from .. import models

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
            scrapedTweets = PyQuery(json['items_html'])
            #Remove incomplete tweets withheld by Twitter Guidelines
            scrapedTweets.remove('div.withheld-tweet')
            tweets = scrapedTweets('div.js-stream-tweet')

            if len(tweets) == 0:
                break

            for tweetHTML in tweets:
                tweetPQ = PyQuery(tweetHTML)
                tweet = models.Tweet()

                uTweet = tweetPQ("span.username.u-dir.u-textTruncate b").text()
                if (' ' in uTweet) == True:
                    # split and get first index
                    usernameTweet = uTweet.split(' ')[0]
                else:
                    usernameTweet = uTweet
                emojis = []
                i = 0
                for emoji in tweetPQ("p.js-tweet-text img"):
                    try:
                        em = emoji.attrib["alt"]
                        emojis.append(em)
                    except KeyError:
                        pass
                textScrap = tweetPQ("div.js-tweet-text-container p.js-tweet-text")
                text = textScrap.html()
                while(re.search(r'<img.*?alt=\"(.*?)\"[^\>]+>', text, flags=re.IGNORECASE)):
                    # replacing img with emojis
                    text = re.sub(r'<img.*?alt=\"(.*?)\"[^\>]+>', emojis[i], text, re.UNICODE)
                    i+=1
                    # print(text + '\n')
                # html tags to python string using beautifulsoup
                text = str(BeautifulSoup(text, features='lxml').get_text()).replace('\n', ' ')
                # text = text.replace('\n', ' ')
                retweets = int(tweetPQ("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""))
                favorites = int(tweetPQ("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""))
                dateSec = int(tweetPQ("small.time span.js-short-timestamp").attr("data-time"))
                id = tweetPQ.attr("data-tweet-id")
                permalink = tweetPQ.attr("data-permalink-path")
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

                tweet.text = text
                tweet.date = datetime.datetime.fromtimestamp(dateSec)
                tweet.formatted_date = datetime.datetime.fromtimestamp(dateSec).strftime("%a %b %d %X +0000 %Y")
                tweet.retweets = retweets
                tweet.favorites = favorites
                tweet.mentions = " ".join(re.compile('(@\\w*)').findall(tweet.text))
                tweet.hashtags = " ".join(re.compile('(#\\w*)').findall(tweet.text))
                tweet.geo = geo
                tweet.emojis = " ".join(emojis)
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
        url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&%smax_position=%s"

        urlGetData = ''
        if hasattr(tweetCriteria, 'username'):
            urlGetData += ' from:' + tweetCriteria.username

        if hasattr(tweetCriteria, 'since'):
            urlGetData += ' since:' + tweetCriteria.since

        if hasattr(tweetCriteria, 'until'):
            urlGetData += ' until:' + tweetCriteria.until

        if hasattr(tweetCriteria, 'querySearch'):
            urlGetData += ' ' + tweetCriteria.querySearch

        if hasattr(tweetCriteria, 'lang'):
            urlLang = 'l=' + tweetCriteria.lang + '&'

        if hasattr(tweetCriteria, 'near'):
            urlGetData += "&near:" + tweetCriteria.near + " within:" + tweetCriteria.within
        else:
            urlLang = ''
        url = url % (urllib.parse.quote(urlGetData), urlLang, refreshCursor)
        # print(url)

        headers = [
            ('Host', "twitter.com"),
            ('User-Agent', "Chrome/66.0.3359.181"),
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
            print("Twitter weird response. Try to see on browser: https://twitter.com/search?q=%s&src=typd" % urllib.parse.quote(urlGetData))
            print("Unexpected error:", sys.exc_info()[0])
            sys.exit()
            return

        dataJson = json.loads(jsonResponse.decode())

        return dataJson
