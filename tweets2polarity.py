#!/usr/bin/env python3

#======= IMPORTS =======
import argparse
import ndjson
import sys
import os

from polarityComputers.hashtagPolarity import HashtagsPolarity

#======= ARGS ========
parser = argparse.ArgumentParser()
parser.add_argument("model", help="Polarity Computing Class", type=int)
parser.add_argument("tweets", help="tweets as an ndjson file")
parser.add_argument("--limit", help="iteration limit", type=int)
args = parser.parse_args()

#======= Functions ======
def loadTweetsFromNDJson(filepath):
    f = open(filepath)
    content = f.read()
    return ndjson.loads(content)

def validateTweetStructure(tweet):
   return 'hashtags' in tweet 

def writeNDJsonToFile(filepath, content):
    with open(filepath, 'w') as output:
        ndjson.dump(content, output)

def defineOutputFilename(model):
    basename = 'tweetsWithPolarity'
    extension = 'json'

    if (0 == model):
        return "{}-{}.{}".format(basename, 'hashtags', extension)

def main():
    if (0 == args.model):
        polarisationFile = os.path.dirname(os.path.abspath(__file__)) + '/polarityCsv/Polarisation.csv'
        polarityComputer = HashtagsPolarity(polarisationFile)
    else:
        print("Available models : \n")
        print("0 - Hashtags")
        sys.exit()

    print("Loading tweets from {}".format(args.tweets))

    tweets = loadTweetsFromNDJson(args.tweets)
    tweetsWithPolarity = []
    outputFile = defineOutputFilename(args.model)
    limit = args.limit if args.limit else len(tweets)

    i = 0
    for tweet in tweets:
        print('Processing tweet {}'.format(i))

        if not validateTweetStructure(tweet):
            print('-- invalid --')
            continue

        print('-- passing --')


        scores = polarityComputer.getPolarityScores(tweet.get('hashtags'))

        if (scores[0] == scores[1]):
            tweet['polarity'] = 'neutral'
        elif (scores[0] > scores[1]):
            tweet['polarity'] = 'positive'
        else:
            tweet['polarity'] = 'negative'

        tweetsWithPolarity.append(tweet)

        i += 1

        if i == limit:
            break

    print('Processed {}/{}'.format(len(tweetsWithPolarity), len(tweets)))
    print('Writing processed tweets to {}'.format(outputFile)) 
    writeNDJsonToFile(outputFile, tweetsWithPolarity)
    


#======= Main =======
main()