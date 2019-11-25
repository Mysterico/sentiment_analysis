from util.tokenize import Tokenize
from util.summarize import Summarize
from konlpy import tag as tagger


class SentimentAnalysisError(Exception):
    pass

class SentimentAnalysis(object):

    def __init__(self):
        try:
            pass
        except SentimentAnalysisError as e:
            print(e)