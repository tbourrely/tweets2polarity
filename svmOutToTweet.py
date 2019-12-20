#!/usr/bin/env python3

import argparse
import ndjson

#========= ARGS =========
parser = argparse.ArgumentParser()
parser.add_argument("tweets", help="Tweets (ndjson file)")
parser.add_argument("svmOutput", help="SVM output file")
parser.add_argument("output", help="Output file (ndjson)")
args = parser.parse_args()


labels = ('objective', 'negative', 'positive', 'mixed')

def writeNDJsonToFile(filepath, content):
    with open(filepath, 'w') as output:
        ndjson.dump(content, output)

def loadTweetsFromNDJson(filepath):
    f = open(filepath)
    content = f.read()
    return ndjson.loads(content)

with open(args.svmOutput, 'r') as svmOutput:

    svmOutputLines = svmOutput.readlines()
    tweets = loadTweetsFromNDJson(args.tweets)

    for i in range(0, len(svmOutputLines)):
        scoreIndex = int(svmOutputLines[i].rstrip())
        label = labels[scoreIndex]

        tweets[i]['polarity'] = label
        

    writeNDJsonToFile(args.output, tweets)