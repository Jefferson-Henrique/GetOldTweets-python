#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, getopt
if sys.version_info[0] < 3:
    raise Exception("Python 2.x is not supported. Please upgrade to 3.x")
import got

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
        opts, args = getopt.getopt(argv, "", ("username=",
                                              "usernames-from-file=",
                                              "near=",
                                              "within=",
                                              "since=",
                                              "until=",
                                              "querysearch=",
                                              "toptweets",
                                              "maxtweets=",
                                              "output="))

        tweetCriteria = got.manager.TweetCriteria()
        outputFileName = "output_got.csv"

        usernames = set()
        username_files = set()
        for opt, arg in opts:
            if opt == '--username':
                usernames_ = [u.lstrip('@') for u in re.split(r'[\s,]+', arg) if u]
                usernames_ = [u.lower() for u in usernames_ if u]
                usernames |= set(usernames_)

            if opt == '--usernames-from-file':
                username_files.add(arg)

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

        if username_files:
            for uf in username_files:
                if not os.path.isfile(uf):
                    raise Exception("File not found: %s"%uf)
                with open(uf) as f:
                    data = f.read()
                    data = re.sub('(?m)#.*?$', '', data)  # remove comments
                    usernames_ = [u.lstrip('@') for u in re.split(r'[\s,]+', data) if u]
                    usernames_ = [u.lower() for u in usernames_ if u]
                    usernames |= set(usernames_)
                    print("Found %i usernames in %s" % (len(usernames_), uf))

        if usernames:
            if len(usernames) > 1:
                tweetCriteria.username = usernames
                if len(usernames)>20 and hasattr(tweetCriteria, 'maxTweets'):
                    maxtweets_ = (len(usernames) // 20 + (len(usernames)%20>0)) * tweetCriteria.maxTweets
                    print("Warning: due to multiple username batches `maxtweets' set to %i" % maxtweets_)
            else:
                tweetCriteria.username = usernames.pop()

        outputFile = open(outputFileName, "w+", encoding="utf8")
        outputFile.write('date,username,retweets,favorites,text,geo,mentions,hashtags,id,permalink\n')

        cnt = 0
        def receiveBuffer(tweets):
            nonlocal cnt

            for t in tweets:
                data = [t.date.strftime("%Y-%m-%d %H:%M:%S"),
                    t.username,
                    t.to or '',
                    t.retweets,
                    t.favorites,
                    '"'+t.text.replace('"','""')+'"',
                    t.geo,
                    t.mentions,
                    t.hashtags,
                    t.id,
                    t.permalink]
                data[:] = [i if isinstance(i, str) else str(i) for i in data]
                outputFile.write(','.join(data) + '\n')

            outputFile.flush()
            cnt += len(tweets)

            if sys.stdout.isatty():
                print("\rSaved %i"%cnt, end='', flush=True)
            else:
                print(cnt, end=' ', flush=True)

        print("Downloading tweets...")
        got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

    except getopt.GetoptError as err:
        print('Arguments parser error, try -h')
        print('\t' + str(err))

    except Exception as err:
        print(str(err))

    finally:
        if "outputFile" in locals():
            outputFile.close()
            print()
            print('Done. Output file generated "%s".' % outputFileName)

if __name__ == '__main__':
    main(sys.argv[1:])
