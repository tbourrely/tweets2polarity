from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer

class TextBlobPolarity:
    def __init__(self):
        pass

    def getPolarityScores(self, sentence):
        blob = TextBlob(sentence, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())

        return blob.sentiment
