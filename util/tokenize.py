from konlpy.tag import Okt

class Tokenize:
    def __init__(self, sentence):
        try:
            if isinstance(sentence, str) is True:
                self.sentence = sentence
                self.okt = Okt()
            else:
                print("Not String")
                raise TypeError("You can't use it if it is not string.")
        except AttributeError as e:
            print(e)

    def tokenize(self):
        tokenize_sentence = self.okt.morphs(self.sentence)
        return tokenize_sentence