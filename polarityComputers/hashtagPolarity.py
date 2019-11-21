class HashtagsPolarity:
    def __init__(self, hashtagsDatabaseFilepath):

        """
        hashtagsDatabase format : CSV
            Hashtag, Polarity, ...
        """
        
        processedCSV = hashtagsFromCSV(hashtagsDatabaseFilepath)
        self.positiveHashtags = processedCSV[0]
        self.negativeHashtags = processedCSV[1]


    def hashtagsFromCSV(self, csvPath):
        return [[], []]

    """
    Input Arguments: self (provided by default), hashtags must be a list
    Returns: a list, the first element is the positivity score,  
                the latter is the negativity score
    """
    def getPolarityScores(self, hashtags):

        return [0.9, 4.2]
