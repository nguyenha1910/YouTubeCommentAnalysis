import gensim
from gensim.models import Phrases
import warnings
warnings.filterwarnings("ignore")

class CommentCorpus:
    def __init__(self, cmmt_list):
        self.cmmt_list = cmmt_list
        self.tk_list = [cmt.split() for cmt in self.cmmt_list]
        self.dict = gensim.corpora.Dictionary(self.tk_list)

    def tokenize(self):
        return self.tk_list

    def bigram(self, min_count=1000):
        bigram = Phrases(self.tk_list, min_count=min_count, delimiter=b'_')
        return [bigram[x] for x in self.tk_list]

    def dictionary(self, save=True, directory = "dictionary"):
        if save:
            self.dict.save(directory)
        return self.dict

    def bag_of_word(self, allow_update = True):
        bow = [self.dict.doc2bow(tks, allow_update=allow_update) for tks in self.tk_list]
        return bow

