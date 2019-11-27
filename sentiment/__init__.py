import tensorflow as tf
import numpy as np
from konlpy.tag import Okt
import os
import json
import nltk
import langdetect

from util.summarize import Summarize

okt = Okt()

class NotSupportLanguageError(Exception):
    print("This language is not supported by this library.")

class SentimentAnalysis(object):

    def __init__(self, sentence):
        try:
            self.sentence = sentence
            self.detected_language = langdetect.detect(sentence)

            if self.detected_language == "ko":
                if os.path.isfile('../data/train_docs.json'):
                    with open('../data/train_docs.json', encoding="utf-8") as f:
                        self.train_docs = json.load(f)
                        self.tokens = [t for d in self.train_docs for t in d[0]]
                        self.text = nltk.Text(self.tokens, name='NMSC')
                        self.selected_words = [f[0] for f in self.text.vocab().most_common(300)]

                self.model = tf.keras.models.load_model("../data/my_model.h5")

            elif self.detected_language == "en":
                if os.path.isfile('../data/train_docs_en.json'):
                    with open('../data/train_docs_en.json', encoding="utf-8") as f:
                        self.train_docs = json.load(f)
                        self.tokens = [t for d in self.train_docs for t in d[0]]
                        self.text = nltk.Text(self.tokens, name='NMSC')
                        self.selected_words = [f[0] for f in self.text.vocab().most_common(1000)]

                self.model = tf.keras.models.load_model("../data/my_model_en.h5")
        except Exception as e:
            print(e)

    def tokenize(self, doc):
        if self.detected_language == "ko":
            return ['/'.join(t) for t in okt.pos(doc, norm=True, stem=True)]
        elif self.detected_language == "en":
            return [''.join(t) for t in nltk.word_tokenize(doc)]

    def term_frequency(self, doc):
        return [doc.count(word) for word in self.selected_words]

    def get_sadness_score(self):
        if self.detected_language == "ko":
            return self.prediction[0]
        elif self.detected_language == "en":
            return self.prediction[1]

    def get_anger_score(self):
        if self.detected_language == "ko":
            return self.prediction[1]
        elif self.detected_language == "en":
            return self.prediction[3]

    def get_anxiety_score(self):
        if self.detected_language == "ko":
            return self.prediction[2]
        elif self.detected_language == "en":
            return self.prediction[12]

    def get_agony_score(self):
        if self.detected_language == "ko":
            return self.prediction[3]
        elif self.detected_language == "en":
            raise NotSupportLanguageError

    def get_embarrassed_score(self):
        if self.detected_language == "ko":
            return self.prediction[4]
        elif self.detected_language == "en":
            return self.prediction[11]

    def get_happiness_score(self):
        if self.detected_language == "ko":
            return self.prediction[5]
        elif self.detected_language == "en":
            return self.prediction[7]

    def get_positive_score(self):
        if self.detected_language == "ko":
            return self.prediction[5]
        elif self.detected_language == "en":
            return self.prediction[5] + self.prediction[6] + self.prediction[7] \
                   + self.prediction[9] + self.prediction[10] + self.prediction[11]

    def get_negative_score(self):
        if self.detected_language == "ko":
            return self.prediction[0] + \
                   self.prediction[1] + \
                   self.prediction[2] + \
                   self.prediction[3] + \
                   self.prediction[4]
        elif self.detected_language == "en":
            return self.prediction[1] + self.prediction[2] + self.prediction[3] \
                   + self.prediction[4] + self.prediction[8] + self.prediction[12]

    def get_neutral_score(self):
        if self.detected_language == "ko":
            raise NotSupportLanguageError
        elif self.detected_language == "en":
            return self.prediction[0]

    def get_total_score(self):
        return self.prediction

    def analyze(self):

        if self.detected_language == "ko":
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

        elif self.detected_language == "en":
            token = self.tokenize(self.sentence)
            tf = self.term_frequency(token)
            data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)
            prediction = self.model.predict(data)[0]

            neutral = prediction[0]
            sadness = prediction[1]
            boredom = prediction[2]
            anger = prediction[3]
            empty = prediction[4]
            enthusiasm = prediction[5]
            fun = prediction[6]
            happiness = prediction[7]
            hate = prediction[8]
            love = prediction[9]
            relief = prediction[10]
            surprise = prediction[11]
            worry = prediction[12]

            emotion_sum = sum(prediction)

            self.neutral_percent = (neutral / emotion_sum) * 100
            self.sadness_percent = (sadness / emotion_sum) * 100
            self.boredom_percent = (boredom / emotion_sum) * 100
            self.anger_percent = (anger / emotion_sum) * 100
            self.empty_percent = (empty / emotion_sum) * 100
            self.enthusiasm_percent = (enthusiasm / emotion_sum) * 100
            self.fun_percent = (fun / emotion_sum) * 100
            self.happiness_percent = (happiness / emotion_sum) * 100
            self.hate_percent = (hate / emotion_sum) * 100
            self.love_percent = (love / emotion_sum) * 100
            self.relief_percent = (relief / emotion_sum) * 100
            self.surprise_percent = (surprise / emotion_sum) * 100
            self.worry_percent = (worry / emotion_sum) * 100

            self.prediction = [round((neutral / emotion_sum) * 100, 2),
                               round((sadness / emotion_sum) * 100, 2),
                               round((boredom / emotion_sum) * 100, 2),
                               round((anger / emotion_sum) * 100, 2),
                               round((empty / emotion_sum) * 100, 2),
                               round((enthusiasm / emotion_sum) * 100, 2),
                               round((fun / emotion_sum) * 100, 2),
                               round((happiness / emotion_sum) * 100, 2),
                               round((hate / emotion_sum) * 100, 2),
                               round((love / emotion_sum) * 100, 2),
                               round((relief / emotion_sum) * 100, 2),
                               round((surprise / emotion_sum) * 100, 2),
                               round((worry / emotion_sum) * 100, 2)]

        # # 0 >> 슬픔 1 >> 분노 2 >> 불안 3 >> 상처 4 >> 당황 5 >> 기쁨