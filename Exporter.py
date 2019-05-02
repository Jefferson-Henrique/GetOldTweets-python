# -*- coding: utf-8 -*-
import sys
import getopt
import csv

if sys.version_info[0] < 3:
    import got
else:
    import got3 as got


def main(argv):
    if len(argv) == 0:
        print('You must pass some parameters. Use \"-h\" to help.')
        return

    if len(argv) == 1 and argv[0] == '-h':
        f = open('exporter_help_text.txt', 'r')
        print(f.read())
        f.close()

        return

    try:
        opts, args = getopt.getopt(argv, "", (
        "username=", "near=", "within=", "since=", "until=", "querysearch=", "toptweets", "maxtweets=", "output=", "lang="))

        tweetCriteria = got.manager.TweetCriteria()
        outputFileName = "output_got.csv"

        for opt, arg in opts:
            if opt == '--username':
                tweetCriteria.username = arg

            elif opt == '--since':
                tweetCriteria.since = arg

            elif opt == '--until':
                tweetCriteria.until = arg

            elif opt == '--querysearch':
                tweetCriteria.querySearch = arg

            elif opt == '--toptweets':
                tweetCriteria.topTweets = True

            elif opt == '--maxtweets':
                tweetCriteria.maxTweets = int(arg)

            elif opt == '--near':
                tweetCriteria.near = '"' + arg + '"'

            elif opt == '--within':
                tweetCriteria.within = '"' + arg + '"'

            elif opt == '--output':
                outputFileName = arg

            elif opt == '--lang':
                tweetCriteria.lang = arg

        outputFile = csv.writer(open(outputFileName, "w", encoding='utf-8-sig', newline=''), delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        outputFile.writerow(
            # ['username','date','retweets','favorites','text','mentions','hashtags','id','permalink', 'emoji'])
            ['username','date','retweets','favorites','text','geo','mentions','hashtags','id','permalink', 'emoji'])

        print('Collecting tweets...\n')

        def receiveBuffer(tweets):
            for t in tweets:
                # print("> Tweets :" + t.text + "\n\n")
                add_list = []
                # print(t.emojis)
                if (isinstance(t.emojis, list)):
                    emoji = ' '.join(t.emojis)
                else:
                    emoji = t.emojis
                # print(emoji)
                # print(t.text)
                for each in [t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink, emoji]:
                # for each in [t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.mentions, t.hashtags, t.id, t.permalink, emoji]:
                    # if type(each) is str:
                    #     for ch in each:
                    #         # if ord(ch) in range(128):
                    #         ch+=ch
                    #     # print("valid_s : " + valid_s)
                    #     add_list.append(ch)
                    # else:
                    add_list.append(each)
                # print(add_list)
                # print('\n\n\n\n')
                outputFile.writerow(add_list)
            print('%d tweets saved on file...\n' % len(tweets))

        got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

    except arg:
        print('Arguments parse error, try -h' + arg)
    finally:
        print('Done. Output file generated "%s".' % outputFileName)


if __name__ == '__main__':
    main(sys.argv[1:])
