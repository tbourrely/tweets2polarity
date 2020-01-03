#!/usr/bin/env python3

#======= IMPORTS =======
import argparse
import ndjson
import sys
import os

import pandas as pd
pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_rows', 500)
import ndjson
import numpy as np
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
import nltk

NLTK_DIR = './nltk_data/'

nltk.data.path.append(NLTK_DIR)
nltk.download('stopwords', download_dir=NLTK_DIR)
nltk.download('punkt', download_dir=NLTK_DIR)

from polarityComputers.hashtagPolarity import HashtagsPolarity
from polarityComputers.TextblobPolarity import TextBlobPolarity

#======= ARGS ========
parser = argparse.ArgumentParser()
parser.add_argument("tweets", help="tweets as an ndjson file")
parser.add_argument("version", help="Polarisation file version", type=int)
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

def removeStopWordsFromMessage(dataframe):
    stop_words = set(stopwords.words('french'))
    dataframe['message'] = dataframe['message'].apply(lambda x: ' '.join([item for item in word_tokenize(x) if item not in stop_words]))
    return dataframe

def removeVariousTwitterElementsFromMessage(dataframe):
    regex_filter = "(@[a-zA-ZÀ-ÿ0-9]+)|(#[a-zA-ZÀ-ÿ0-9]+)"
    dataframe['message'] = dataframe['message'].apply(lambda x: ' '.join(re.sub(regex_filter, ' ', x).split()))
    return dataframe

def removeUrlsFromMessage(dataframe):
    dataframe['message'] = dataframe['message'].apply(lambda x: re.split('https?:\/\/.*', str(x))[0])
    return dataframe

def getOnlyAlphaFromMessage(dataframe):
    dataframe['message'] = dataframe['message'].apply(lambda x: ' '.join([word.lower() for word in word_tokenize(x) if word.isalpha()]))
    return dataframe

def prepareDataframeMessage(dataframe_source):
    df = dataframe_source.copy()
    return (df
            .pipe(removeUrlsFromMessage)
            .pipe(removeVariousTwitterElementsFromMessage)
            .pipe(getOnlyAlphaFromMessage)
            .pipe(removeStopWordsFromMessage)
            )

def listToCleanDataframe(source_data):
    # load tweets in pandas dataframe
    dataframe = pd.DataFrame(source_data)
    cleaned_dataframe = prepareDataframeMessage(dataframe)

    dataframe['clean_message'] = cleaned_dataframe['message']

    return dataframe

def main():
    print("Loading tweets from {}".format(args.tweets))

    tweets = loadTweetsFromNDJson(args.tweets)
    outputFile = 'annotated-tweets.json'

    tweetsWithPolarity = []
    availablePolarities = {
            'mixte': 'mixte',
            'positif': 'positif',
            'negatif': 'negatif',
            'autre': 'autre'
        }

    limit = args.limit if args.limit else len(tweets)
    
    polarisationFile = os.path.dirname(os.path.abspath(__file__)) + '/polarityCsv/PolarisationV{}.csv'.format(args.version)
    hashtagsPolarityComputer = HashtagsPolarity(polarisationFile)
    testBlobPolarityComputer = TextBlobPolarity()

    # create a dataframe containing collumn from json and a new one with cleaned message
    tweetsDataframe = listToCleanDataframe(tweets)

    i = 0

    for index, row in tweetsDataframe.iterrows():
        print('Processing tweet {}'.format(index))

        if not validateTweetStructure(row):
            print('-- invalid --')
            continue

        print('-- passing --')

        print('message : {}'.format(row['message']))

        hashtagsPositive, hashtagsNegative = hashtagsPolarityComputer.getPolarityScores(row['hashtags'])
        
        textblocPolarity, textblobSubjectivity = testBlobPolarityComputer.getPolarityScores(row['clean_message'])
        textblocPositive = 0 if textblocPolarity <= 0 else textblocPolarity
        textblocNegative = 0 if textblocPolarity >= 0 else abs(textblocPolarity)

        print('Hasgtags scores : pos {} neg {}'.format(hashtagsPositive, hashtagsNegative))
        print('Textblob scores : polarity : {} subjectivity {} Pos {} Neg {}'.format(textblocPolarity, textblobSubjectivity, textblocPositive, textblocNegative))


        totalPositive = hashtagsPositive * 0.33 + textblocPositive
        totalNegative = hashtagsNegative * 0.33 + textblocNegative

        print('Total pos {} neg {}'.format(totalPositive, totalNegative))

        if totalPositive == totalNegative and totalPositive == 0 and totalNegative == 0:
            polarity = availablePolarities['autre']
        elif totalPositive > totalNegative:
            polarity = availablePolarities['positif']
        elif totalPositive < totalNegative:
            polarity = availablePolarities['negatif']
        else:
            polarity = availablePolarities['mixte']

        print('Polarity : {}'.format(polarity))
            
        row['polarity'] = polarity

        tweetsWithPolarity.append(row.to_dict())
        

        i += 1

        if i == limit:
            break


    print('Processed {}/{}'.format(len(tweetsWithPolarity), len(tweets)))
    print('Writing processed tweets to {}'.format(outputFile)) 
    writeNDJsonToFile(outputFile, tweetsWithPolarity)
    


#======= Main =======
main()
