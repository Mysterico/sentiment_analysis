# Sentiment_analysis (감성 분석)
일기 및 일상 평문 텍스트에서, 글쓴이의 감정을 유추하기 위해서 만들어진 라이브러리입니다. 감성 분석을 위해서,
Keras 및 nltk가 사용되었습니다. 또한, 텍스트의 길이에 따라서 문장을 요약하고 이에 대한 감성을 각각 분석을 하기 위해
Lexrank 알고리즘이 사용되었습니다.

해당 라이브러리는 감성을 다음 6가지의 종류로 분류합니다. (우울함, 분노, 불안, 고통, 당황, 행복)

This library is made for analyzing sentiment from a single sentence or paragraph. It uses Keras and nltk.
In addition, It also uses LexRank algorithm to summarize a paragraph.

It classifies sentiment as 6 emotions (Depression, Anger, Anxiety, Agony, Embarrassed, Happiness)

※ Caution)

This library does not support English or other languages yet. However, we have a plan to support other languages includes English, Japanese, Chinese, and etc. 

## Installation
`pip install sentiment-analysis`

## Usage
```python
from sentiment import SentimentAnalysis
sentiment_analysis = SentimentAnalysis(want_to_analyze_sentence_or_paragraph)
sentiment_analysis.analyze() # It initializes analysis progress

sadness_score = sentiment_analysis.get_sadness_score() # get depression score.
anger_score = sentiment_analysis.get_anger_score() # get anger score.
anxiety_score = sentiment_analysis.get_anxiety_score() # get anxiety score.
agony_score = sentiment_analysis.get_agony_score() # get agony score.
embarrassed_score = sentiment_analysis.get_embarrassed_score() # get embarrassed score.
happiness_score = sentiment_analysis.get_happiness_score() # get happiness score.

total_score = sentiment_analysis.get_total_score() # get all scores as list type.

```

### Reference)
1. https://github.com/theeluwin/lexrankr (Korean Lexrank)
