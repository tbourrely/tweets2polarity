#!/usr/bin/env python3

import csv
import ndjson
import os

def writeNDJsonToFile(filepath, content):
    with open(filepath, 'w') as output:
        ndjson.dump(content, output)

input_file = os.path.dirname(os.path.realpath(__file__)) + '/test.txt'
output_file='test-euapv.json'

tweets = []

with open(input_file, newline='', encoding='utf-8') as file:
    line = file.readline()

    while line:
        splitted = line.split()

        identifier = splitted[0]
        message = ' '.join(splitted[1:])

        tweets.append({
            'identifier': identifier,
            'message': message,
            'polarity': None
        })
        
        line = file.readline()
    