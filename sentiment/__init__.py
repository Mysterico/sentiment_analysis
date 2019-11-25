import tensorflow as tf
import numpy as np
from konlpy.tag import Okt
import os
import json
import nltk

from util.summarize import Summarize
from lexrankr import LexRank

okt = Okt()


model = tf.keras.models.load_model("my_model.h5")
model.summary()

class SentimentAnalysis(object):

    def __init__(self, sentence):
        try:
            if os.path.isfile('train_docs.json'):
                with open('train_docs.json', encoding="utf-8") as f:
                    self.train_docs = json.load(f)
                    self.tokens = [t for d in self.train_docs for t in d[0]]
                    self.text = nltk.Text(self.tokens, name='NMSC')
                    self.selected_words = [f[0] for f in self.text.vocab().most_common(300)]

            self.sentence = sentence
            self.model = tf.keras.models.load_model("my_model.h5")
        except Exception as e:
            print(e)

    def tokenize(self, doc):
        return ['/'.join(t) for t in okt.pos(doc, norm=True, stem=True)]

    def term_frequency(self, doc):
        return [doc.count(word) for word in self.selected_words]

    def get_sadness_score(self):
        return self.prediction[0]

    def get_anger_score(self):
        return self.prediction[1]

    def get_anxiety_score(self):
        return self.prediction[2]

    def get_agony_score(self):
        return self.prediction[3]

    def get_embarrassed_score(self):
        return self.prediction[4]

    def get_happiness_score(self):
        return self.prediction[5]

    def analyze(self, text):

        sadness_sum = 0
        anger_sum = 0
        anxiety_sum = 0
        agony_sum = 0
        embarrassed_sum = 0
        happiness_sum = 0

        summarized_data = Summarize(text).summarize()

        for text in summarized_data:
            token = self.tokenize(text)
            tf = self.term_frequency(token)
            data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)

            prediction = model.predict(data)[0]

            sadness_sum += prediction[0]
            anger_sum += prediction[1]
            anxiety_sum += prediction[2]
            agony_sum += prediction[3]
            embarrassed_sum += prediction[4]
            happiness_sum += prediction[5]

        self.prediction = [sadness_sum / 5, anger_sum / 5, anxiety_sum / 5, agony_sum / 5, embarrassed_sum / 5, happiness_sum / 5]
        return self.prediction # # 0 >> 슬픔 1 >> 분노 2 >> 불안 3 >> 상처 4 >> 당황 5 >> 기쁨