import csv

class HashtagsPolarity:
    def __init__(self, hashtagsDatabaseFilepath):

        """
        hashtagsDatabase format : CSV
            Hashtag, Polarity, ...
        """
        
        processedCSV = self.hashtagsFromCSV(hashtagsDatabaseFilepath)
        self.positiveHashtags = processedCSV[0]
        self.negativeHashtags = processedCSV[1]


    def hashtagsFromCSV(self, csvPath):
        positive = []
        negative = []

        with open(csvPath, 'r') as f:
            reader = csv.reader(f, delimiter=';')

            for row in reader:
                if 'positif' == row[1]:
                    positive.append(row[0])
                elif 'negatif' == row[1]:
                    negative.append(row[0])

        return [positive, negative]

    def isPositive(self, hashtag):
        return hashtag in self.positiveHashtags

    def isNegative(self, hashtag):
        return hashtag in self.negativeHashtags

    """
    Input Arguments: self (provided by default), hashtags must be a list
    Returns: a list, the first element is the positivity score,  
                the latter is the negativity score
    """
    def getPolarityScores(self, hashtags):
        positiveScore = 0 
        negativeScore = 0

        for hashtag in hashtags:
            if self.isPositive(hashtag):
                positiveScore += 1

            if self.isNegative(hashtag):
                negativeScore += 1

        return [positiveScore, negativeScore]
