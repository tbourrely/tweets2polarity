#!/usr/bin/env python3

import argparse
import ndjson
from os import path

#========= ARGS =========
parser = argparse.ArgumentParser()
parser.add_argument("--training", help="Training file")
parser.add_argument("--test", help="Test file")
args = parser.parse_args()

def loadTweetsFromNDJson(filepath):
    f = open(filepath)
    content = f.read()
    return ndjson.loads(content)

def save(fileName, content):
    f = open(fileName, 'w')
    f.write(content)
    f.close()
    print("Wrote in {}".format(fileName))

def prepareWordListAndLabels(tweets):
    words = [False] # index must start at 1
    labels = []

    for tweet in tweets:
        label = tweet['polarity']
        message = tweet['message']

        for word in message.split():
            if word not in words:
                words.append(word)

        if label not in labels:
            labels.append(label)

    return (words, labels)

def formatForSVM(tweets, words, labels):
    output = ''

    for tweet in tweets:
        message = tweet['message']
        label = tweet['polarity']

        wordsInTweet = {}

        for word in message.split():
            if word in wordsInTweet:
                wordsInTweet[word][1] += 1
            else:
                wordsInTweet[word] = [words.index(word), 1]

        orderedWordsInTweet = sorted(wordsInTweet.items(), key=lambda x: x[1][0])

        rowOutput = '{}'.format(labels.index(label))

        for word, stats in orderedWordsInTweet:
            rowOutput += ' {}:{}'.format(stats[0], stats[1])

        rowOutput += '\n'

        output += rowOutput

    return output



trainingOutput = 'train.svm'
testOutput = 'test.svm'

trainTweets = loadTweetsFromNDJson(args.training) if args.training else None
testTweets = loadTweetsFromNDJson(args.test) if args.test else None

trainingWords = []
trainingLabels = []
testWords = []
testLabels = []

if trainTweets:
    print('Preparing training wordlist and labels')
    trainingWords, trainingLabels = prepareWordListAndLabels(trainTweets)
    print('Train : {} words, {} labels'.format(len(trainingWords), len(trainingLabels)))

if testTweets:
    print('Preparing test wordlist and labels')
    testWords, testLabels = prepareWordListAndLabels(testTweets)
    print('Test : {} words, {} labels'.format(len(testWords), len(testLabels)))

words = list(set(trainingWords + testWords)) # merge without duplicates
labels = list(set(trainingLabels + testLabels)) # merge without duplicates

print('Merge result : {} words, {} labels'.format(len(words), len(labels)))
print('Labels : ')
for i in range(0, len(labels)):
    print('{}) {}'.format(i, labels[i]))

if trainTweets:
    print('Formatting training data')
    svmFormattedTraining = formatForSVM(trainTweets, words, labels)
    save(trainingOutput, svmFormattedTraining)

if testTweets:
    print('Formatting test data')
    svmFormattedTesting = formatForSVM(testTweets, words, labels)
    save(testOutput, svmFormattedTesting)