import json, re, ndjson

file = "convertjson.json"
outfile = "processedTweets.json"

regex = "(#[-0-9a-zÀ-ÿA-Z]*)"

i = 1

f = open(file)
content = f.read()
jsonContent = json.loads(content)

tweetsList = jsonContent['tweet']

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
