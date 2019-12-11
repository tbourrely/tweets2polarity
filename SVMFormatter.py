#!/usr/bin/env python3

import argparse
import ndjson
from os import path

#========= ARGS =========
parser = argparse.ArgumentParser()
parser.add_argument("training", help="Training file", type=int)
parser.add_argument("test", help="Test file")
args = parser.parse_args()

trainingOutput = 'train.svm'
testOutput = 'test.svm'