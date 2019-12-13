#!/usr/bin/env python3

import argparse

#========= ARGS =========
parser = argparse.ArgumentParser()
parser.add_argument("test", help="File containing test data (from euapv)")
parser.add_argument("svmOut", help="SVM out file")
args = parser.parse_args()


def save(fileName, content):
    f = open(fileName, 'w')
    f.write(content)
    f.close()
    print("Wrote in {}".format(fileName))

lines = ''
out = 'svm_results.txt'
labels = ('negatif', 'positif', 'autre')

with open(args.svmOut, 'r') as svmOut:
    with open(args.test, 'r') as testFile:

        svmOutLines = svmOut.readlines()
        testFileLines = testFile.readlines()

        if (len(svmOutLines) != len(testFileLines)):
            print('Files not same length')
        else:
            for i in range(0, len(svmOutLines)):
                scoreId = int(svmOutLines[i].rstrip())
                score = labels[scoreId]
                identifier = testFileLines[i].split()[0]

                lines += '{} {}\n'.format(identifier, score)

save(out, lines)