import json, re, ndjson
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("fileinput", help="tweets as an ndjson file")
args = parser.parse_args()

file = args.fileinput
outfile = "processedTweets.json"

regex = "(#[-0-9a-zÀ-ÿA-Z]*)"

i = 1

f = open(file)
content = f.read()
jsonContent = ndjson.loads(content)

tweetsList = jsonContent

processedTweets = []

for tweet in tweetsList:
    hashtags = re.findall(regex, tweet.get('message'))

    tweet['hashtags'] = hashtags

    processedTweets.append(tweet)

    print("processed {}".format(i))

    #if i == 100:
    #    break

    i = i + 1


with open(outfile, 'w') as outputStream:
    ndjson.dump(processedTweets, outputStream)
