import tensorflow as tf
import pandas as pd
import os
import json
import nltk
import numpy as np

from konlpy.tag import Okt

okt = Okt()

models = tf.keras.models
layers = tf.keras.layers
optimizers = tf.keras.optimizers
losses = tf.keras.losses
metrics = tf.keras.metrics

def read_data(filename):
    file = pd.read_excel(filename)
    return file

def tokenize(doc):
    return ['/'.join(t) for t in okt.pos(doc, norm=True, stem=True)]

def term_frequency(doc):
    return [doc.count(word) for word in selected_words]

def predict_post_neg(text):
    token = tokenize(text)
    tf = term_frequency(token)
    data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)
    prediction = model.predict(data)
    return prediction

train_data = read_data("sentiment_data_ko.xlsx")
test_data = read_data("sentiment_data_test_ko.xlsx")

if os.path.isfile('train_docs.json'):
    with open('train_docs.json', encoding="utf-8") as f:
        train_docs = json.load(f)
    with open('test_docs.json', encoding="utf-8") as f:
        test_docs = json.load(f)
else:
    train_docs = [(tokenize(data[0]), data[1]) for data in train_data.to_numpy()]
    test_docs = [(tokenize(data[0]), data[1]) for data in test_data.to_numpy()]
    # JSON 파일로 저장
    with open('train_docs.json', 'w', encoding="utf-8") as make_file:
        json.dump(train_docs, make_file, ensure_ascii=False, indent="\t")
    with open('test_docs.json', 'w', encoding="utf-8") as make_file:
        json.dump(test_docs, make_file, ensure_ascii=False, indent="\t")

tokens = [t for d in train_docs for t in d[0]]
text = nltk.Text(tokens, name='NMSC')
selected_words = [f[0] for f in text.vocab().most_common(300)]

train_x = [term_frequency(d) for d, _ in train_docs]
test_x = [term_frequency(d) for d, _ in test_docs]
train_y = [c for _, c in train_docs]
test_y = [c for _, c in test_docs]

x_train = np.asarray(train_x).astype('float32')
x_test = np.asarray(test_x).astype('float32')

y_train = np.asarray(train_y).astype('float32')
y_test = np.asarray(test_y).astype('float32')

model = models.Sequential()
model.add(layers.Dense(32, activation='relu', input_shape=(179,)))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(6, activation='sigmoid'))

model.compile(optimizer=optimizers.Adam(lr=0.001),
              loss=losses.sparse_categorical_crossentropy,
              metrics=[metrics.categorical_accuracy])

model.fit(x_train, y_train, epochs=30, batch_size=10)
model.save("my_model.h5")

model = tf.keras.models.load_model("my_model.h5")
model.summary()

prediction = predict_post_neg("저는 행복합니다. 계속 이 날이 지속됐으면 좋겠어요. 이 행복한 감정을 계속 느끼고 싶어요.")[0]

sadness = prediction[0]
anger = prediction[1]
anxiety = prediction[2]
hurt = prediction[3]
embarrassed = prediction[4]
happiness = prediction[5]

emotion_sum = sum(prediction)

sadness_percent = (sadness / emotion_sum) * 100
anger_percent = (anger / emotion_sum) * 100
anxiety_percent = (anxiety / emotion_sum) * 100
hurt_percent = (hurt / emotion_sum) * 100
embarrassed_percent = (embarrassed / emotion_sum) * 100
happiness_percent = (happiness / emotion_sum) * 100

print("현재 당신의 감정에는 슬픔이 {}%, 분노가 {}%, 불안이 {}%, 상처가 {}%, 당황스러움이 {}%, 행복함이 {}%로 나타났습니다.".format(round(sadness_percent, 2), round(anger_percent, 2), round(anxiety_percent, 2), round(hurt_percent, 2), round(embarrassed_percent, 2), round(happiness_percent, 2)))

# 0 >> 슬픔
# 1 >> 분노
# 2 >> 불안
# 3 >> 상처
# 4 >> 당황
# 5 >> 기쁨
