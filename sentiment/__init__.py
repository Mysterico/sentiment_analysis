import tensorflow as tf
import numpy as np
from konlpy.tag import Okt
import os
import json
import nltk

from util.summarize import Summarize

okt = Okt()

class SentimentAnalysis(object):

    def __init__(self, sentence):
        try:
            if os.path.isfile('../data/train_docs.json'):
                with open('../data/train_docs.json', encoding="utf-8") as f:
                    self.train_docs = json.load(f)
                    self.tokens = [t for d in self.train_docs for t in d[0]]
                    self.text = nltk.Text(self.tokens, name='NMSC')
                    self.selected_words = [f[0] for f in self.text.vocab().most_common(300)]

            self.sentence = sentence
            self.model = tf.keras.models.load_model("../data/my_model.h5")
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

    def get_total_score(self):
        return self.prediction

    def analyze(self):

        sadness_sum = 0
        anger_sum = 0
        anxiety_sum = 0
        agony_sum = 0
        embarrassed_sum = 0
        happiness_sum = 0

        summarized_data = Summarize(self.sentence).summarize()

        for text in summarized_data:
            token = self.tokenize(text)
            tf = self.term_frequency(token)
            data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)

            prediction = self.model.predict(data)[0]

            sadness_sum += prediction[0]
            anger_sum += prediction[1]
            anxiety_sum += prediction[2]
            agony_sum += prediction[3]
            embarrassed_sum += prediction[4]
            happiness_sum += prediction[5]


        total_sum = sadness_sum + anger_sum + anxiety_sum + agony_sum + embarrassed_sum + happiness_sum

        self.prediction = [round(((sadness_sum / total_sum)) * 100, 2),
                           round(((anger_sum / total_sum)) * 100, 2),
                           round(((anxiety_sum / total_sum)) * 100, 2),
                           round(((agony_sum / total_sum)) * 100, 2),
                           round(((embarrassed_sum / total_sum)) * 100, 2),
                           round(((happiness_sum / total_sum)) * 100, 2)]

        # # 0 >> 슬픔 1 >> 분노 2 >> 불안 3 >> 상처 4 >> 당황 5 >> 기쁨