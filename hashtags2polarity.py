#!/usr/bin/env python3

#======= IMPORTS =======
import argparse
import ndjson

#======= ARGS ========
parser = argparse.ArgumentParser()
parser.add_argument("tweets", help="tweets as an ndjson file")
args = parser.parse_args()

#======= Functions ======
def loadTweetsFromNDJson(filepath):
    f = open(filepath)
    content = f.read()
    return ndjson.loads(content)

def validateTweetStructure(tweet):
   return 'hashtags' in tweet 

def main():
    print("Loading tweets from {}".format(args.tweets))

    tweets = loadTweetsFromNDJson(args.tweets)
    tweetsWithPolarity = []

    i = 0
    for tweet in tweets:
        print('Processing tweet {}'.format(i))

        if not validateTweetStructure(tweet):
            print('-- invalid --')
            continue

        print('-- passing --')

        i += 1

        if i == 10:
            break


#======= Main =======
main()
