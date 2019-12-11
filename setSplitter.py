#!/usr/bin/env python3

import argparse
import ndjson
from os import path

#========= ARGS =========
parser = argparse.ArgumentParser()
parser.add_argument("file", help="File ")
parser.add_argument("training", help="Training set percentage", type=int)
parser.add_argument("--validation", help="Validation set percentage", type=int)
parser.add_argument("test", help="Test set percentage", type=int)
args = parser.parse_args()

#======= Functions ======
def loadTweetsFromNDJson(filepath):
    f = open(filepath)
    content = f.read()
    return ndjson.loads(content)

def writeNDJsonToFile(filepath, content):
    with open(filepath, 'w') as output:
        ndjson.dump(content, output)

tweets = loadTweetsFromNDJson(args.file)
tweetsLength = len(tweets)

validationPercentage = args.validation if args.validation else 0

outputDir = path.dirname(args.file)
traningOutput = outputDir + '/training.json'
validationOutput = outputDir + '/validation.json'
testOutput = outputDir + '/test.json'

trainingLength = int(tweetsLength * args.training / 100)
testLength = int(tweetsLength * args.test / 100)
validationLength = int(tweetsLength * validationPercentage / 100)

trainingTweets = tweets[:trainingLength]
validationTweets = tweets[trainingLength + 1:trainingLength + validationLength] if validationLength != 0 else None
testTweets = tweets[trainingLength + validationLength + 1: trainingLength + validationLength + testLength]

print('training : ' + str(len(trainingTweets)))
print('validation : {}'.format(str(len(validationTweets)) if validationTweets else 'None') )
print('test : ' + str(len(testTweets)))

writeNDJsonToFile(traningOutput, trainingTweets)
writeNDJsonToFile(testOutput, testTweets)

if validationTweets:
    writeNDJsonToFile(validationOutput, validationTweets)

print('----------------------------')
print('training: {}'.format(traningOutput))
print('validation: {}'.format(validationOutput if validationTweets else 'None'))
print('test: {}'.format(testOutput))
print('----------------------------')