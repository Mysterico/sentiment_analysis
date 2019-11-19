from lexrankr import LexRank

class Summarize:
    def __init__(self, paragraph):
        try:
            if isinstance(paragraph, str) is True:
                self.paragraph = paragraph
                self.probe_num = 0
        except AttributeError as e:
            raise TypeError("You can't use it if it is not string.")

    def summarize(self):
        lex = LexRank()
        lex.summarize(self.paragraph)

        if len(self.paragraph) < 100:
            self.probe_num = 1
        elif len(self.paragraph) < 200:
            self.probe_num = 2
        elif len(self.paragraph) < 300:
            self.probe_num = 3
        elif len(self.paragraph) < 400:
            self.probe_num = 4
        else:
            self.probe_num = 5

        summaries = lex.probe(self.probe_num)
        return summaries
