from collections import defaultdict
import warnings

warnings.filterwarnings("ignore")


class WordAssociation:
    def __init__(self, dictionary, bow_list):
        self.dict = dictionary
        self.bow_list = bow_list
        self.term_freq = defaultdict(int)
        self.co_freq_collection = defaultdict(dict)
        # co_freq_collection is a dictionary where the key is a token, and
        # value is the co_freq dict associated with that key
        # co_freq dict saves the frequency of all words
        # that co-appear with the token
        self.pmi_collection = defaultdict(dict)

    def gen_term_freq(self):
        for bow in self.bow_list:
            for t in set([b[0] for b in bow]):
                self.term_freq[t] += 1
        return self.term_freq

    def gen_co_freq(self, token):
        co_freq = defaultdict(int)
        token_id = self.dict.token2id[token]
        for bow in self.bow_list:
            unique = set([b[0] for b in bow])
            for t in unique:
                if token_id in unique and token_id != t:
                    co_freq[t] += 1
        self.co_freq_collection[token] = co_freq
        return co_freq

    def token_pmi(self, token, threshold=100):
        if token not in self.co_freq_collection:
            self.co_freq_collection[token] = self.gen_co_freq(token)
        co_freq = self.co_freq_collection[token]
        if token not in self.term_freq:
            self.term_freq = self.gen_term_freq()
        pmi = defaultdict(int)
        for ck in co_freq:
            if self.term_freq[ck] > threshold:
                pmi[ck] = co_freq[ck] / self.term_freq[ck]
        self.pmi_collection[token] = pmi
        return pmi

    def get_top_kw(self, token, top=1):
        score_list = [(i, f) for i, f in self.pmi_collection[token].items()]
        score_list = sorted(score_list, key=lambda x: x[1], reverse=True)
        score_list = score_list[:int(len(score_list) * top)]
        return score_list
