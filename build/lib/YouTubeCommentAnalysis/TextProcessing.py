import emoji
import re
from bs4 import BeautifulSoup
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer
import warnings
warnings.filterwarnings("ignore")

def str_join(tokens):
    """Join tokens into a long string"""
    return ' '.join(tokens)

class TextProcessing:
    """Process raw comments file crawled from Youtube API to get clean text"""

    def __init__(self):
        pass

    def process_text(self, text):
        """Strip punctuations, links, tags, and demojize string"""
        result = str(text)
        soup = BeautifulSoup(result)
        result = soup.get_text()
        result = result.lower()
        # Strip punctuation, link
        result = re.sub(r'!|"|“|”|$|%|&|\\|\'|\’|\(|\)|\*|\+|,|-|\.|\/|:|;|<|=|>|\?|\^|_|`|{|}|~|\||(http\S+)|(href\S+)',
                        ' ', str(result))
        # Demoji
        result = emoji.demojize(result)
        result = re.sub(r'(:\w+?:)', ' \\1 ', str(result))
        return result

    def lemmatize_stemming(self, text):
        """Lemmatize a list of tokens"""
        tokens = text.split()
        tokens = [t for t in tokens if len(t) >= 3]
        tokens = [t for t in tokens if t not in STOPWORDS]
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(tk, pos='v') for tk in tokens]
        tokens = str_join(tokens)
        return tokens

    def deEmojify(self, text):
        """deemojify text"""
        regrex_pattern = re.compile(pattern="["
                                            u"\U0001F600-\U0001F64F"  # emoticons
                                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                            "]+", flags=re.UNICODE)
        if text:
            return regrex_pattern.sub(r'', str(text))
        return text

    def isEnglish(self, text):
        """Check is text is in English
        Return True or False"""
        text = self.deEmojify(text)
        try:
            text.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        return True

